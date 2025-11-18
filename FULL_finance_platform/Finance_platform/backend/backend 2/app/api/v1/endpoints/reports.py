"""Reporting API endpoints - placeholder."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def list_reports():
    """List reports - TODO: Implement reporting."""
    return {"message": "Reporting coming soon"}
