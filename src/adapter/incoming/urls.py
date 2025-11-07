from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse

from src.adapter.incoming.api.long_url import LongUrl
from src.dependencies import shortening_service

router = APIRouter(
    prefix="/urls",
    tags=["urls"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def all_urls():
    return await shortening_service.list()


@router.get("/{short_code}")
async def original_url(short_code: str):
    try:
        result = await shortening_service.get_original_url(short_code)
        if not result:
            raise HTTPException(status_code=404, detail="URL not found")
        return RedirectResponse(result, status_code=302)
    except Exception as inst:
        print(f"Couldn't find URL with short code '{short_code}' due to error {inst}")
        raise HTTPException(
            status_code=404, detail=f"URL not found for short code '{short_code}'"
        )


@router.post(
    "/",
    status_code=201,
)
async def short_url(long_url: LongUrl, request: Request):
    short_code: str = await shortening_service.shorten(long_url.url)
    return f"{request.url}{short_code}"
