from fastapi import APIRouter, HTTPException
from Models.Schemas import ArchitectureRequest, ArchitectureResponse
from Services.Gemini_service import design_architecture

router = APIRouter(prefix="/api/architecture", tags=["Architecture"])


@router.post("/", response_model=ArchitectureResponse, summary="Design project architecture")
async def create_architecture(req: ArchitectureRequest):
    """
    Design a practical tech architecture for your hackathon project.

    Returns layer breakdown, data flow, deployment plan, API endpoints,
    and estimated setup time — all tailored to your team's skills and constraints.
    """
    try:
        return await design_architecture(req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini error: {str(e)}")