"""
FastAPI Integration for Excel Model Generation
Provides REST API endpoints to generate models from the Portfolio Dashboard
"""

from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel, UUID4
from typing import Optional, List
from datetime import datetime
import os
import logging

from excel_model_generator import (
    DCFModelGenerator,
    LBOModelGenerator,
    MergerModelGenerator,
    BatchModelGenerator
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Portfolio Dashboard - Model Generator API")


# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class ModelGenerationRequest(BaseModel):
    """Request to generate a single model"""
    company_id: UUID4
    model_type: str  # 'DCF', 'LBO', 'Merger', 'DD', 'QoE'
    scenario_name: Optional[str] = "Base Case"
    
    class Config:
        json_schema_extra = {
            "example": {
                "company_id": "123e4567-e89b-12d3-a456-426614174000",
                "model_type": "DCF",
                "scenario_name": "Base Case"
            }
        }


class MergerModelRequest(BaseModel):
    """Request to generate merger model (requires 2 companies)"""
    acquirer_id: UUID4
    target_id: UUID4
    scenario_name: Optional[str] = "Base Case"


class BatchGenerationRequest(BaseModel):
    """Request to generate all models for a company"""
    company_id: UUID4
    models: Optional[List[str]] = ['DCF', 'LBO', 'DD', 'QoE']


class ModelGenerationResponse(BaseModel):
    """Response after model generation"""
    success: bool
    model_type: str
    file_path: str
    company_name: str
    generated_at: datetime
    message: Optional[str] = None


class BatchGenerationResponse(BaseModel):
    """Response for batch generation"""
    success: bool
    company_id: str
    company_name: str
    models_generated: dict
    total_models: int
    successful_models: int
    failed_models: int


# ============================================================================
# DATABASE DEPENDENCY
# ============================================================================

def get_db():
    """Database session dependency"""
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    
    # This would come from environment variable
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://portfolio_user:password@localhost/portfolio_db')
    
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/")
def root():
    """API root endpoint"""
    return {
        "name": "Portfolio Dashboard Model Generator API",
        "version": "1.0.0",
        "endpoints": {
            "generate_single": "/api/v1/models/generate",
            "generate_batch": "/api/v1/models/generate-batch",
            "generate_merger": "/api/v1/models/generate-merger",
            "download": "/api/v1/models/download/{file_name}",
            "list_models": "/api/v1/models/list/{company_id}"
        }
    }


@app.post("/api/v1/models/generate", response_model=ModelGenerationResponse)
def generate_model(
    request: ModelGenerationRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Generate a single financial model for a company
    
    Supported model types:
    - DCF: Discounted Cash Flow model
    - LBO: Leveraged Buyout model
    - DD: Due Diligence tracker
    - QoE: Quality of Earnings analysis
    """
    try:
        company_id = str(request.company_id)
        model_type = request.model_type.upper()
        
        # Validate model type
        valid_types = ['DCF', 'LBO', 'DD', 'QOE']
        if model_type not in valid_types:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid model type. Must be one of: {', '.join(valid_types)}"
            )
        
        # Generate output directory
        output_dir = '/home/claude/generated_models'
        os.makedirs(output_dir, exist_ok=True)
        
        # Get company info
        from excel_model_generator import PortfolioCompany
        company = db.query(PortfolioCompany).filter(
            PortfolioCompany.company_id == company_id
        ).first()
        
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")
        
        company_slug = company.company_name.replace(' ', '_').replace('/', '_')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Generate model
        file_path = None
        
        if model_type == 'DCF':
            generator = DCFModelGenerator(db, company_id)
            file_path = f'{output_dir}/{company_slug}_DCF_{timestamp}.xlsx'
            generator.generate(file_path)
        
        elif model_type == 'LBO':
            generator = LBOModelGenerator(db, company_id)
            file_path = f'{output_dir}/{company_slug}_LBO_{timestamp}.xlsx'
            generator.generate(file_path)
        
        # TODO: Add DD and QoE generators
        
        return ModelGenerationResponse(
            success=True,
            model_type=model_type,
            file_path=file_path,
            company_name=company.company_name,
            generated_at=datetime.now(),
            message=f"{model_type} model generated successfully"
        )
    
    except Exception as e:
        logger.error(f"Model generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/models/generate-merger", response_model=ModelGenerationResponse)
def generate_merger_model(
    request: MergerModelRequest,
    db: Session = Depends(get_db)
):
    """
    Generate a Merger & Acquisition model
    Requires both acquirer and target company IDs
    """
    try:
        acquirer_id = str(request.acquirer_id)
        target_id = str(request.target_id)
        
        # Get company info
        from excel_model_generator import PortfolioCompany
        acquirer = db.query(PortfolioCompany).filter(
            PortfolioCompany.company_id == acquirer_id
        ).first()
        
        target = db.query(PortfolioCompany).filter(
            PortfolioCompany.company_id == target_id
        ).first()
        
        if not acquirer or not target:
            raise HTTPException(status_code=404, detail="Acquirer or target company not found")
        
        # Generate output
        output_dir = '/home/claude/generated_models'
        os.makedirs(output_dir, exist_ok=True)
        
        company_slug = f"{acquirer.company_name}_acquiring_{target.company_name}".replace(' ', '_').replace('/', '_')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        file_path = f'{output_dir}/{company_slug}_Merger_{timestamp}.xlsx'
        
        # Generate model
        generator = MergerModelGenerator(db, acquirer_id, target_id)
        generator.generate(file_path)
        
        return ModelGenerationResponse(
            success=True,
            model_type='Merger',
            file_path=file_path,
            company_name=f"{acquirer.company_name} + {target.company_name}",
            generated_at=datetime.now(),
            message="Merger model generated successfully"
        )
    
    except Exception as e:
        logger.error(f"Merger model generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/models/generate-batch", response_model=BatchGenerationResponse)
def generate_batch_models(
    request: BatchGenerationRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Generate multiple models for a company at once
    This runs as a background task for large batches
    """
    try:
        company_id = str(request.company_id)
        
        # Get company info
        from excel_model_generator import PortfolioCompany
        company = db.query(PortfolioCompany).filter(
            PortfolioCompany.company_id == company_id
        ).first()
        
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")
        
        # Generate all models
        generator = BatchModelGenerator(db)
        results = generator.generate_all_models(company_id)
        
        # Count successes
        successful = sum(1 for v in results.values() if v is not None)
        failed = len(results) - successful
        
        return BatchGenerationResponse(
            success=(failed == 0),
            company_id=company_id,
            company_name=company.company_name,
            models_generated=results,
            total_models=len(results),
            successful_models=successful,
            failed_models=failed
        )
    
    except Exception as e:
        logger.error(f"Batch generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/models/download/{file_name}")
def download_model(file_name: str):
    """
    Download a generated model file
    """
    file_path = f'/home/claude/generated_models/{file_name}'
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=file_path,
        filename=file_name,
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )


@app.get("/api/v1/models/list/{company_id}")
def list_generated_models(company_id: str, db: Session = Depends(get_db)):
    """
    List all generated models for a company
    """
    # Get company info
    from excel_model_generator import PortfolioCompany
    company = db.query(PortfolioCompany).filter(
        PortfolioCompany.company_id == company_id
    ).first()
    
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    company_slug = company.company_name.replace(' ', '_').replace('/', '_')
    output_dir = '/home/claude/generated_models'
    
    # List files
    if not os.path.exists(output_dir):
        return {"company_id": company_id, "models": []}
    
    files = [
        f for f in os.listdir(output_dir)
        if f.startswith(company_slug) and f.endswith('.xlsx')
    ]
    
    models = []
    for file in files:
        file_path = os.path.join(output_dir, file)
        stat = os.stat(file_path)
        
        # Extract model type from filename
        model_type = 'Unknown'
        for type_name in ['DCF', 'LBO', 'Merger', 'DD', 'QoE']:
            if type_name in file:
                model_type = type_name
                break
        
        models.append({
            'file_name': file,
            'model_type': model_type,
            'file_size': stat.st_size,
            'created_at': datetime.fromtimestamp(stat.st_ctime).isoformat(),
            'download_url': f'/api/v1/models/download/{file}'
        })
    
    return {
        'company_id': company_id,
        'company_name': company.company_name,
        'total_models': len(models),
        'models': sorted(models, key=lambda x: x['created_at'], reverse=True)
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


# ============================================================================
# STARTUP EVENT
# ============================================================================

@app.on_event("startup")
def startup_event():
    """Initialize on startup"""
    logger.info("Model Generator API starting up...")
    
    # Create output directory
    os.makedirs('/home/claude/generated_models', exist_ok=True)
    
    logger.info("API ready to generate models!")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
