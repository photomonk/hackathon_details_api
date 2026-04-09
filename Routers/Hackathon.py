from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from Models.Schemas import HackathonSearchRequest, HackathonSearchResponse, HackathonFormat
from Services.Gemini_service import get_hackathon_events





router = APIRouter(prefix="/api/hackathons", tags=["Hackathons"])


@router.get("/", response_model=HackathonSearchResponse, summary="Find hackathon events")
async def search_hackathons(
    theme: str = Query(..., example="AI / ML", description="Theme or domain"),
    format: HackathonFormat = Query(HackathonFormat.any),
    skill_level: Optional[str] = Query(None, example="beginner"),
    extra: Optional[str] = Query(None, description="Extra preferences"),
):
    """
    Find relevant hackathon events and platforms based on your interests.

    Returns 4 tailored event suggestions with tips.
    """
    try:
        req = HackathonSearchRequest(
            theme=theme,
            format=format,
            skill_level=skill_level,
            extra=extra,
        )
        return await get_hackathon_events(req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini error: {str(e)}")


@router.post("/", response_model=HackathonSearchResponse, summary="Find hackathon events (POST)")
async def search_hackathons_post(req: HackathonSearchRequest):
    """POST version — useful when sending more detailed preferences."""
    try:
        return await get_hackathon_events(req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini error: {str(e)}")