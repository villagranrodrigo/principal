"""FastAPI routes exposing the patient summary pipeline."""
from __future__ import annotations

from typing import List, Optional

from fastapi import Body, FastAPI, HTTPException, Path
from pydantic import BaseModel

from .models import PatientIntakeData, SummaryVersion
from .pipeline import PatientSummaryPipeline
from .store import SummaryStore
from .summarizer import TemplateSummarizer

app = FastAPI(title="Patient Summary Service", version="1.0.0")

pipeline = PatientSummaryPipeline(summarizer=TemplateSummarizer(), store=SummaryStore())


class SummaryRevisionRequest(BaseModel):
    """Request payload when recording a revision to an existing summary."""

    intake_id: str
    notes: str
    summary_text: Optional[str] = None


@app.post("/summaries/propose", response_model=SummaryVersion)
async def propose_summary(intake: PatientIntakeData) -> SummaryVersion:
    """Generate a new summary draft for the supplied intake information."""

    return pipeline.propose_summary(intake)


@app.post("/summaries/{intake_id}/revise", response_model=SummaryVersion)
async def revise_summary(
    intake_id: str = Path(..., description="Identifier of the intake to revise"),
    payload: SummaryRevisionRequest = Body(...),
) -> SummaryVersion:
    """Persist a revised summary version and accompanying notes."""

    if intake_id != payload.intake_id:
        raise HTTPException(status_code=400, detail="Path and payload intake IDs must match")
    try:
        return pipeline.revise_summary(
            intake_id=intake_id,
            notes=payload.notes,
            summary_text=payload.summary_text,
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/summaries/{intake_id}/diffs")
async def get_diffs(intake_id: str = Path(..., description="Identifier of the intake")) -> List[dict]:
    """Retrieve line-by-line diffs between summary versions."""

    if not pipeline.store.has_intake(intake_id):
        raise HTTPException(status_code=404, detail="Intake not found")
    return pipeline.compare_versions(intake_id)


@app.get("/corpus")
async def get_corpus() -> List[dict]:
    """Return corpus entries composed of intake data and summary versions."""

    return pipeline.collect_training_corpus()
