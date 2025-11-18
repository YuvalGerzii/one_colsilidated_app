"""Model generation API endpoints - placeholder."""

from fastapi import APIRouter

router = APIRouter()


@router.post("/generate")
def generate_model():
    """Generate Excel model - TODO: Integrate model generator."""
    return {"message": "Model generation coming soon"}


@router.post("/generate-batch")
def generate_batch():
    """Generate all models - TODO: Integrate batch generator."""
    return {"message": "Batch generation coming soon"}
