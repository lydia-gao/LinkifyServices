from fastapi import HTTPException, status
from fastapi.responses import RedirectResponse

def redirect_to_original(obj):

    if not obj:
        raise HTTPException(status_code=404, detail="Resource not found")
    return RedirectResponse(
        url=obj.original_url,
        status_code=status.HTTP_307_TEMPORARY_REDIRECT
    )
