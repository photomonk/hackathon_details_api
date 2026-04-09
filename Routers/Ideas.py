from fastapi import APIRouter, HTTPException
from Models.Schemas import IdeaRequest, IdeaResponse
from Services.Gemini_service import generate_ideas

router = APIRouter(prefix="/api/ideas", tags=["Ideas"])


@router.post("/", response_model=IdeaResponse, summary="Generate hackathon project ideas")
async def create_ideas(req: IdeaRequest):
    """
    Generate 3 creative, buildable hackathon project ideas.

    Tailored to your team's skills, theme, and available time.
    Returns a recommended idea and actionable tips.
    """
    try:
        return await generate_ideas(req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini error: {str(e)}")