import json
import re
import os
from google import genai
from dotenv import load_dotenv
from Models.Schemas import (
    HackathonSearchRequest, HackathonSearchResponse,
    IdeaRequest, IdeaResponse,
    ArchitectureRequest, ArchitectureResponse,
)

# Load environment variables
load_dotenv()


class HackathonAgent:
    """Internal Agent to handle Gemini 2.0 Client and logic."""
    
    def __init__(self):
        self.model_name = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
        api_key = os.getenv("GEMINI_API_KEY")
        
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables.")
            
        self.client = genai.Client(api_key=api_key)
        self.system_instruction = (
            "You are an elite hackathon mentor and technical architect. "
            "Your goal is to provide highly actionable, buildable, and "
            "competitive advice for developers in high-pressure environments."
        )

    def _call(self, prompt: str, is_json: bool = True) -> dict:
        """Executes the LLM request with JSON enforcement."""
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config={
                "system_instruction": self.system_instruction,
                "temperature": 0.7,
                "response_mime_type": "application/json" if is_json else "text/plain"
            }
        )
        
        raw_text = response.text.strip()
        
        if is_json:
            try:
                # Cleanup potential markdown fences
                clean_json = re.sub(r"```json\n?|```", "", raw_text)
                return json.loads(clean_json)
            except json.JSONDecodeError:
                return {"error": "Failed to parse model response", "raw": raw_text}
        
        return {"text": raw_text}

# --- Internal Singleton Instance ---
_agent = HackathonAgent()

# --- Public API Functions ---

async def get_hackathon_events(req: HackathonSearchRequest) -> HackathonSearchResponse:
    """
    Public function to suggest relevant hackathon events based on user search criteria.
    """
    prompt = f"""
    Suggest 4 relevant hackathon events based on:
    Theme: {req.theme} | Format: {req.format.value} | Skill: {req.skill_level or 'any'}
    Extra: {req.extra or 'none'}

    Return JSON matching:
    {{
      "query_summary": "string",
      "events": [
        {{ "name": "string", "platform": "string", "theme": "string", 
           "format": "string", "duration": "string", "prize_range": "string", 
           "difficulty": "string", "why_good_fit": "string" }}
      ],
      "tips": ["string"]
    }}
    """
    data = _agent._call(prompt)
    return HackathonSearchResponse(**data)

async def generate_ideas(req: IdeaRequest) -> IdeaResponse:
    """
    Public function to generate creative and buildable project ideas for a team.
    """
    prompt = f"""
    Generate 3 unique project ideas for a {req.duration_hours} hour hackathon.
    Theme: {req.theme} | Skills: {", ".join(req.skills)} | Team Size: {req.team_size.value}
    
    Return JSON matching:
    {{
      "theme": "{req.theme}",
      "ideas": [
        {{ "title": "string", "tagline": "string", "problem_solved": "string", 
           "core_features": ["list"], "tech_stack": ["list"], 
           "mvp_scope": "string", "wow_factor": "string", "difficulty": "string" }}
      ],
      "recommended_idea": "title",
      "quick_tip": "string"
    }}
    """
    data = _agent._call(prompt)
    return IdeaResponse(**data)

async def design_architecture(req: ArchitectureRequest) -> ArchitectureResponse:
    """
    Public function to design a full technical architecture and deployment plan.
    """
    prompt = f"""
    Design a deployable architecture for: {req.project_title}
    Description: {req.description} | Skills: {", ".join(req.skills)}
    Constraints: {req.constraints or 'none'}

    Return JSON matching:
    {{
      "project_title": "{req.project_title}",
      "architecture_style": "string",
      "layers": [{{ "name": "string", "technology": "string", "purpose": "string", "free_tier": true }}],
      "data_flow": ["step1", "step2"],
      "deployment_plan": "string",
      "estimated_setup_time": "string",
      "api_endpoints": ["string"],
      "challenges_to_watch": ["string"]
    }}
    """
    data = _agent._call(prompt)
    return ArchitectureResponse(**data)