from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum


# ─── Shared ────────────────────────────────────────────────────────────────────

class HackathonFormat(str, Enum):
    remote = "remote"
    in_person = "in-person"
    hybrid = "hybrid"
    any = "any"


class TeamSize(str, Enum):
    solo = "solo"
    small = "small"       # 2-3
    medium = "medium"     # 4-6
    large = "large"       # 7+
    any = "any"


# ─── /api/hackathons ───────────────────────────────────────────────────────────

class HackathonSearchRequest(BaseModel):
    theme: str = Field(..., example="AI / ML", description="Main theme or domain")
    format: HackathonFormat = Field(HackathonFormat.any, description="Event format")
    skill_level: Optional[str] = Field(None, example="beginner", description="Beginner / intermediate / advanced")
    extra: Optional[str] = Field(None, description="Any extra preferences or context")


class HackathonEvent(BaseModel):
    name: str
    platform: str
    theme: str
    format: str
    duration: str
    prize_range: str
    difficulty: str
    why_good_fit: str


class HackathonSearchResponse(BaseModel):
    query_summary: str
    events: List[HackathonEvent]
    tips: List[str]


# ─── /api/ideas ────────────────────────────────────────────────────────────────

class IdeaRequest(BaseModel):
    theme: str = Field(..., example="mental health", description="Hackathon theme / problem domain")
    skills: List[str] = Field(..., example=["Python", "React", "AI/ML"])
    team_size: TeamSize = Field(TeamSize.medium)
    duration_hours: int = Field(24, ge=6, le=72, description="Hackathon duration in hours")
    extra: Optional[str] = Field(None, description="Any extra constraints or preferences")


class ProjectIdea(BaseModel):
    title: str
    tagline: str
    problem_solved: str
    core_features: List[str]
    tech_stack: List[str]
    mvp_scope: str
    wow_factor: str
    difficulty: str


class IdeaResponse(BaseModel):
    theme: str
    ideas: List[ProjectIdea]
    recommended_idea: str
    quick_tip: str


# ─── /api/architecture ─────────────────────────────────────────────────────────

class ArchitectureRequest(BaseModel):
    project_title: str = Field(..., example="AI Carpooling App")
    description: str = Field(..., description="What the project does")
    skills: List[str] = Field(..., example=["React", "Python", "PostgreSQL"])
    constraints: Optional[str] = Field(None, description="Free-tier only, deploy in 24h, etc.")
    team_size: TeamSize = Field(TeamSize.medium)


class ServiceLayer(BaseModel):
    name: str
    technology: str
    purpose: str
    free_tier: bool


class ArchitectureResponse(BaseModel):
    project_title: str
    architecture_style: str
    layers: List[ServiceLayer]
    data_flow: List[str]
    deployment_plan: str
    estimated_setup_time: str
    api_endpoints: List[str]
    challenges_to_watch: List[str]