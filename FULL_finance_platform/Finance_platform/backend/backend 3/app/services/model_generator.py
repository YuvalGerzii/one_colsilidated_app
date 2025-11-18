"""Model generation service - TODO: Integrate /mnt/project/excel_model_generator.py"""

from uuid import UUID
from sqlalchemy.orm import Session

class ModelGeneratorService:
    """Service for generating Excel models."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def generate_dcf(self, company_id: UUID, output_path: str) -> str:
        """Generate DCF model - TODO: Implement."""
        pass
    
    def generate_lbo(self, company_id: UUID, output_path: str) -> str:
        """Generate LBO model - TODO: Implement."""
        pass
