"""
Complete PDF Extraction Pipeline
=================================
Full workflow from PDF upload → extraction → validation → database storage

This integrates with the Portfolio Dashboard database schema and provides
API endpoints for the frontend.
"""

import os
import uuid
from typing import Dict, List, Optional
from datetime import datetime
from decimal import Decimal
import json
import logging

# Database imports (pseudo-code - would use SQLAlchemy in production)
# from sqlalchemy import create_engine, Column, String, Numeric, DateTime, Boolean, ForeignKey
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker, relationship

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PDFExtractionPipeline:
    """
    Complete extraction pipeline:
    1. Upload PDF to S3
    2. Extract financial data
    3. Validate extraction
    4. Store in database
    5. Link to company models
    """
    
    def __init__(self, company_id: str, db_session=None, s3_client=None):
        self.company_id = company_id
        self.db = db_session
        self.s3 = s3_client
    
    def process_pdf(self, pdf_path: str, document_type: str, uploaded_by: str) -> Dict:
        """
        Complete PDF processing workflow
        
        Args:
            pdf_path: Local path to PDF file
            document_type: Type of document (e.g., "Financial Statement", "Board Report")
            uploaded_by: User ID who uploaded
            
        Returns:
            Processing result with document_id and extraction status
        """
        logger.info(f"Processing PDF for company {self.company_id}")
        
        result = {
            'document_id': str(uuid.uuid4()),
            'company_id': self.company_id,
            'timestamp': datetime.utcnow().isoformat(),
            'status': 'processing',
            'steps': []
        }
        
        try:
            # Step 1: Upload to S3
            logger.info("Step 1: Uploading to cloud storage...")
            s3_url = self._upload_to_s3(pdf_path, result['document_id'])
            result['steps'].append({
                'step': 'upload',
                'status': 'success',
                'url': s3_url
            })
            
            # Step 2: Create document record
            logger.info("Step 2: Creating document record...")
            doc_record = self._create_document_record(
                result['document_id'],
                os.path.basename(pdf_path),
                document_type,
                s3_url,
                uploaded_by
            )
            result['steps'].append({
                'step': 'document_record',
                'status': 'success',
                'record_id': doc_record['id']
            })
            
            # Step 3: Extract financial data
            logger.info("Step 3: Extracting financial data...")
            from pdf_financial_extractor import extract_financial_statements
            
            extracted_data = extract_financial_statements(pdf_path)
            result['extracted_data'] = extracted_data
            result['steps'].append({
                'step': 'extraction',
                'status': 'success',
                'statements_found': {
                    'income_statements': len(extracted_data.get('income_statements', [])),
                    'balance_sheets': len(extracted_data.get('balance_sheets', [])),
                    'cash_flows': len(extracted_data.get('cash_flows', []))
                }
            })
            
            # Step 4: Validate extracted data
            logger.info("Step 4: Validating extraction...")
            validation_results = self._validate_extraction(extracted_data)
            result['validation'] = validation_results
            result['steps'].append({
                'step': 'validation',
                'status': 'success',
                'needs_review': validation_results['needs_review']
            })
            
            # Step 5: Store in database
            logger.info("Step 5: Storing in database...")
            stored_records = self._store_financial_data(
                result['document_id'],
                extracted_data,
                validation_results
            )
            result['steps'].append({
                'step': 'database_storage',
                'status': 'success',
                'records_created': len(stored_records)
            })
            
            # Step 6: Update company models
            logger.info("Step 6: Triggering model updates...")
            self._trigger_model_updates()
            result['steps'].append({
                'step': 'model_update',
                'status': 'success'
            })
            
            # Mark as complete
            result['status'] = 'completed'
            logger.info(f"PDF processing completed: {result['document_id']}")
            
        except Exception as e:
            logger.error(f"PDF processing failed: {e}")
            result['status'] = 'failed'
            result['error'] = str(e)
            result['steps'].append({
                'step': 'error',
                'status': 'failed',
                'message': str(e)
            })
        
        return result
    
    def _upload_to_s3(self, local_path: str, document_id: str) -> str:
        """Upload PDF to S3 storage"""
        if self.s3:
            bucket = 'portfolio-dashboard-documents'
            key = f"companies/{self.company_id}/pdfs/{document_id}.pdf"
            
            # In production:
            # self.s3.upload_file(local_path, bucket, key)
            # url = f"s3://{bucket}/{key}"
            
            # For now, return mock URL
            url = f"s3://{bucket}/{key}"
            logger.info(f"Uploaded to {url}")
            return url
        else:
            # Local development - just return file path
            return local_path
    
    def _create_document_record(self, doc_id: str, filename: str, doc_type: str, 
                               file_path: str, uploaded_by: str) -> Dict:
        """Create document record in database"""
        if self.db:
            # In production, insert into documents table:
            """
            document = Document(
                document_id=doc_id,
                company_id=self.company_id,
                document_name=filename,
                document_type=doc_type,
                file_path=file_path,
                upload_date=datetime.utcnow(),
                uploaded_by=uploaded_by,
                extraction_status='Processing'
            )
            self.db.add(document)
            self.db.commit()
            """
            pass
        
        # Mock return
        return {
            'id': doc_id,
            'company_id': self.company_id,
            'filename': filename,
            'type': doc_type
        }
    
    def _validate_extraction(self, extracted_data: Dict) -> Dict:
        """Validate extracted financial data"""
        from ai_financial_extractor import ExtractionValidator
        
        validation = {
            'overall_confidence': 0.0,
            'needs_review': False,
            'issues': [],
            'statement_validations': {}
        }
        
        # Validate each income statement
        for idx, stmt in enumerate(extracted_data.get('income_statements', [])):
            is_valid, issues = ExtractionValidator.validate_income_statement(stmt)
            validation['statement_validations'][f'income_{idx}'] = {
                'valid': is_valid,
                'issues': issues,
                'confidence': stmt.get('confidence_score', 0)
            }
            if not is_valid:
                validation['needs_review'] = True
                validation['issues'].extend(issues)
        
        # Validate balance sheets
        for idx, stmt in enumerate(extracted_data.get('balance_sheets', [])):
            is_valid, issues = ExtractionValidator.validate_balance_sheet(stmt)
            validation['statement_validations'][f'balance_{idx}'] = {
                'valid': is_valid,
                'issues': issues,
                'confidence': stmt.get('confidence_score', 0)
            }
            if not is_valid:
                validation['needs_review'] = True
                validation['issues'].extend(issues)
        
        # Calculate overall confidence
        all_confidences = [
            v['confidence'] 
            for v in validation['statement_validations'].values()
        ]
        if all_confidences:
            validation['overall_confidence'] = sum(all_confidences) / len(all_confidences)
        
        # Flag for review if confidence < 85%
        if validation['overall_confidence'] < 0.85:
            validation['needs_review'] = True
            validation['issues'].append(
                f"Low confidence score: {validation['overall_confidence']:.1%}"
            )
        
        return validation
    
    def _store_financial_data(self, document_id: str, extracted_data: Dict,
                              validation: Dict) -> List[str]:
        """Store extracted financial data in database"""
        stored_ids = []
        
        if not self.db:
            logger.warning("No database session - skipping storage")
            return stored_ids
        
        # Store income statements
        for stmt in extracted_data.get('income_statements', []):
            metric_id = self._store_income_statement(document_id, stmt, validation)
            if metric_id:
                stored_ids.append(metric_id)
        
        # Store balance sheets
        for stmt in extracted_data.get('balance_sheets', []):
            metric_id = self._store_balance_sheet(document_id, stmt, validation)
            if metric_id:
                stored_ids.append(metric_id)
        
        # Store cash flows
        for stmt in extracted_data.get('cash_flows', []):
            metric_id = self._store_cash_flow(document_id, stmt, validation)
            if metric_id:
                stored_ids.append(metric_id)
        
        return stored_ids
    
    def _store_income_statement(self, document_id: str, data: Dict, 
                                validation: Dict) -> Optional[str]:
        """Store income statement data in financial_metrics table"""
        if not self.db:
            return None
        
        try:
            metric_id = str(uuid.uuid4())
            
            # Map to database schema
            period = data.get('period', {})
            
            # In production:
            """
            metric = FinancialMetric(
                metric_id=metric_id,
                company_id=self.company_id,
                period_date=period.get('period_date'),
                period_type=period.get('period_type'),
                fiscal_year=period.get('fiscal_year'),
                fiscal_quarter=period.get('fiscal_quarter'),
                
                # Income statement fields
                revenue=data.get('revenue'),
                cost_of_revenue=data.get('cost_of_revenue'),
                gross_profit=data.get('gross_profit'),
                operating_expenses=data.get('operating_expenses'),
                ebitda=data.get('ebitda'),
                depreciation_amortization=data.get('depreciation_amortization'),
                ebit=data.get('ebit'),
                interest_expense=data.get('interest_expense'),
                pretax_income=data.get('pretax_income'),
                tax_expense=data.get('income_tax'),
                net_income=data.get('net_income'),
                
                # Metadata
                source_document_id=document_id,
                data_quality_score=validation['overall_confidence'],
                requires_review=validation['needs_review'],
                created_date=datetime.utcnow(),
                last_updated=datetime.utcnow()
            )
            
            self.db.add(metric)
            self.db.commit()
            """
            
            logger.info(f"Stored income statement: {metric_id}")
            return metric_id
            
        except Exception as e:
            logger.error(f"Failed to store income statement: {e}")
            return None
    
    def _store_balance_sheet(self, document_id: str, data: Dict,
                            validation: Dict) -> Optional[str]:
        """Store balance sheet data"""
        # Similar to income statement storage
        return None
    
    def _store_cash_flow(self, document_id: str, data: Dict,
                        validation: Dict) -> Optional[str]:
        """Store cash flow data"""
        # Similar to income statement storage
        return None
    
    def _trigger_model_updates(self):
        """Trigger regeneration of financial models"""
        if not self.db:
            return
        
        # In production, queue model generation tasks:
        """
        # Update DCF model
        dcf_task = ModelGenerationTask(
            company_id=self.company_id,
            model_type='DCF',
            priority='high',
            status='queued'
        )
        self.db.add(dcf_task)
        
        # Update LBO model
        lbo_task = ModelGenerationTask(
            company_id=self.company_id,
            model_type='LBO',
            priority='medium',
            status='queued'
        )
        self.db.add(lbo_task)
        
        self.db.commit()
        """
        
        logger.info("Model update tasks queued")


# FastAPI endpoints for PDF extraction
class PDFExtractionAPI:
    """
    API endpoints for PDF extraction feature
    
    Usage:
        from fastapi import FastAPI, UploadFile, File, Depends
        from fastapi.responses import JSONResponse
        
        app = FastAPI()
        
        @app.post("/api/v1/companies/{company_id}/documents/upload")
        async def upload_document(...):
            ...
    """
    
    @staticmethod
    def create_endpoints(app):
        """Create API endpoints on FastAPI app"""
        
        @app.post("/api/v1/companies/{company_id}/documents/upload")
        async def upload_financial_document(
            company_id: str,
            file: 'UploadFile',
            document_type: str = "Financial Statement",
            user_id: str = None
        ):
            """
            Upload and process a financial document PDF
            
            Args:
                company_id: UUID of portfolio company
                file: PDF file upload
                document_type: Type of document
                user_id: User who uploaded
                
            Returns:
                JSON with document_id and processing status
            """
            # Save uploaded file
            file_path = f"/tmp/{uuid.uuid4()}_{file.filename}"
            with open(file_path, "wb") as f:
                content = await file.read()
                f.write(content)
            
            try:
                # Process PDF
                pipeline = PDFExtractionPipeline(
                    company_id=company_id,
                    db_session=None,  # Get from dependency
                    s3_client=None    # Get from dependency
                )
                
                result = pipeline.process_pdf(
                    pdf_path=file_path,
                    document_type=document_type,
                    uploaded_by=user_id or "system"
                )
                
                return result
                
            finally:
                # Cleanup
                if os.path.exists(file_path):
                    os.remove(file_path)
        
        @app.get("/api/v1/documents/{document_id}/status")
        async def get_extraction_status(document_id: str):
            """
            Get status of document extraction
            
            Returns:
                Processing status and extracted data
            """
            # In production, query database:
            """
            doc = db.query(Document).filter(
                Document.document_id == document_id
            ).first()
            
            return {
                'document_id': doc.document_id,
                'status': doc.extraction_status,
                'extracted_data': doc.extracted_data,
                'needs_review': doc.needs_review,
                'confidence_score': doc.extraction_confidence
            }
            """
            return {'document_id': document_id, 'status': 'processing'}
        
        @app.post("/api/v1/documents/{document_id}/review")
        async def review_extraction(
            document_id: str,
            corrections: Dict,
            reviewed_by: str
        ):
            """
            Manual review and correction of extracted data
            
            Args:
                document_id: Document to review
                corrections: Dictionary of field corrections
                reviewed_by: User ID of reviewer
                
            Returns:
                Updated extraction status
            """
            # Apply corrections and mark as reviewed
            # Update database with corrected values
            return {'status': 'reviewed', 'document_id': document_id}
        
        return app


# Example: Complete workflow demonstration
def demonstrate_pdf_pipeline():
    """Demonstrate complete PDF extraction pipeline"""
    
    print("=" * 60)
    print("PDF EXTRACTION PIPELINE DEMONSTRATION")
    print("=" * 60)
    
    # Setup
    company_id = "meta-platforms-inc"
    pdf_path = "/mnt/user-data/uploads/Meta-Reports-Third-Quarter-2025-Results-2025.pdf"
    
    # Create pipeline
    pipeline = PDFExtractionPipeline(
        company_id=company_id,
        db_session=None,  # Would connect to real DB in production
        s3_client=None    # Would connect to S3 in production
    )
    
    # Process PDF
    print(f"\nProcessing: {os.path.basename(pdf_path)}")
    print(f"Company: {company_id}")
    print("-" * 60)
    
    result = pipeline.process_pdf(
        pdf_path=pdf_path,
        document_type="Quarterly Earnings Report",
        uploaded_by="demo-user"
    )
    
    # Display results
    print(f"\nStatus: {result['status']}")
    print(f"Document ID: {result['document_id']}")
    print("\nProcessing Steps:")
    for step in result['steps']:
        status_icon = "✓" if step['status'] == 'success' else "✗"
        print(f"  {status_icon} {step['step']}: {step['status']}")
    
    if result.get('validation'):
        val = result['validation']
        print(f"\nValidation:")
        print(f"  Overall Confidence: {val['overall_confidence']:.1%}")
        print(f"  Needs Review: {val['needs_review']}")
        if val['issues']:
            print(f"  Issues Found:")
            for issue in val['issues'][:5]:  # Show first 5
                print(f"    - {issue}")
    
    # Show extracted data summary
    if result.get('extracted_data'):
        data = result['extracted_data']
        print(f"\nExtracted Data Summary:")
        print(f"  Document Type: {data.get('document_type')}")
        print(f"  Periods Found: {len(data.get('periods', []))}")
        print(f"  Income Statements: {len(data.get('income_statements', []))}")
        print(f"  Balance Sheets: {len(data.get('balance_sheets', []))}")
        print(f"  Cash Flow Statements: {len(data.get('cash_flows', []))}")
    
    print("\n" + "=" * 60)
    
    return result


if __name__ == '__main__':
    # Run demonstration
    result = demonstrate_pdf_pipeline()
    
    # Save full results to file
    output_file = '/home/claude/pdf_extraction_result.json'
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2, default=str)
    
    print(f"\nFull results saved to: {output_file}")
