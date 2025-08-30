from fastapi import APIRouter, HTTPException, Query
from pydantic import AnyUrl
from app.utils.metadata_utils import fetch_url_metadata

router = APIRouter(
    prefix="/metadata",
    tags=["metadata"]
)

@router.get("/", status_code=200)
async def get_metadata(url: AnyUrl = Query(..., description="Target URL to fetch metadata")):
    try:
        meta = fetch_url_metadata(str(url))
        return meta
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch metadata: {str(e)}")
