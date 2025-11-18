"""PDF extraction API endpoints - placeholder."""

from fastapi import APIRouter

router = APIRouter()


@router.post("/upload")
def upload_pdf():
    """Upload and extract PDF - TODO: Integrate PDF extractor."""
    return {"message": "PDF extraction coming soon"}
