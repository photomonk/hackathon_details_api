from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

import os
# from config import get_settings
from Routers import Hackathon, Ideas, Architechure


# ─── Lifespan ──────────────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    # settings = get_settings()
    print(f"🚀  Hackathon AI API started  |  env={os.getenv('APP_ENV')}  |  model={os.getenv('GEMINI_MODEL')}")
    yield
    print("👋  Shutting down")


# ─── App ───────────────────────────────────────────────────────────────────────

# settings = get_settings()

app = FastAPI(
    title="Hackathon AI API",
    description=(
        "A Gemini-powered API that helps you find hackathon events, "
        "generate project ideas, and design your project architecture."
    ),
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)


# ─── Middleware ────────────────────────────────────────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # Tighten this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── Routers ───────────────────────────────────────────────────────────────────

app.include_router(Hackathon.router)
app.include_router(Ideas.router)
app.include_router(Architechure.router)


# ─── Root & Health ─────────────────────────────────────────────────────────────

@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Hackathon AI API — powered by Gemini",
        "docs": "/docs",
        "endpoints": {
            "hackathons": "GET  /api/hackathons?theme=AI&format=remote",
            "ideas":      "POST /api/ideas",
            "architecture":"POST /api/architecture",
        },
    }


@app.get("/health", tags=["Root"])
async def health():
    return {"status": "ok", "model": os.getenv("GEMINI_MODEL")}


# ─── Run ───────────────────────────────────────────────────────────────────────
