"""FastAPI application entrypoint."""

from __future__ import annotations

from fastapi import FastAPI

app = FastAPI(title="Esports Tournament API")

# Include routers
from app.controllers.team import router as team_router
from app.controllers.tournament import router as tournament_router
from app.controllers.player import router as player_router
from app.controllers.match import router as match_router

app.include_router(team_router, prefix="/teams")
app.include_router(tournament_router, prefix="/tournaments")
app.include_router(player_router, prefix="/players")
app.include_router(match_router, prefix="/matches")


@app.get("/")
def root() -> dict[str, str]:
    """Health-style root endpoint."""
    return {"message": "Esports Tournament API"}
