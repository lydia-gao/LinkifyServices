from fastapi import APIRouter, HTTPException, Query
from pydantic import AnyUrl
from app.services.metadata_service import fetch_metadata_logic

router = APIRouter(
    prefix="/metadata",
    tags=["metadata"]
)

@router.get("/", status_code=200)
async def get_metadata(url: AnyUrl = Query(..., description="Target URL to fetch metadata")):
    try:
        return fetch_metadata_logic(str(url))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch metadata: {str(e)}")
# Use shared dependencies (if needed for future DB access)
from app.database.dependencies import db_dependency, user_dependency
