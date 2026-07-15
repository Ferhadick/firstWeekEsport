"""FastAPI application entrypoint."""

from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from app.exceptions import (
    AlreadyExistsException,
    BusinessValidationException,
    DatabaseException,
    NotFoundException,
)

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


@app.exception_handler(NotFoundException)
def not_found_handler(request: Request, exc: NotFoundException) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"success": False, "message": exc.message, "details": exc.details},
    )


@app.exception_handler(AlreadyExistsException)
def already_exists_handler(request: Request, exc: AlreadyExistsException) -> JSONResponse:
    return JSONResponse(
        status_code=409,
        content={"success": False, "message": exc.message, "details": exc.details},
    )


@app.exception_handler(BusinessValidationException)
def business_validation_handler(request: Request, exc: BusinessValidationException) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content={"success": False, "message": exc.message, "details": exc.details},
    )


@app.exception_handler(RequestValidationError)
def validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={"success": False, "message": "Validation failed", "errors": exc.errors()},
    )


@app.exception_handler(SQLAlchemyError)
def sqlalchemy_error_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={"success": False, "message": "A database error occurred.", "details": None},
    )


@app.exception_handler(DatabaseException)
def database_exception_handler(request: Request, exc: DatabaseException) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={"success": False, "message": exc.message, "details": exc.details},
    )


@app.exception_handler(Exception)
def general_error_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={"success": False, "message": "An unexpected error occurred.", "details": None},
    )


@app.get("/")
def root() -> dict[str, str]:
    """Health-style root endpoint."""
    return {"message": "Esports Tournament API"}
