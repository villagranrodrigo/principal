"""Domain models for patient summary pipeline."""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class PatientIntakeData(BaseModel):
    """Structured representation of the data captured during patient intake."""

    intake_id: str = Field(..., description="Unique identifier for the intake session")
    patient_name: str = Field(..., description="Full name of the patient")
    age: int = Field(..., ge=0, description="Age of the patient")
    chief_complaint: str = Field(..., description="Primary reason for the visit")
    history: Optional[str] = Field(
        default="",
        description="Pertinent medical history or context gathered during intake",
    )
    medications: Optional[str] = Field(
        default="",
        description="Current medications the patient is taking",
    )


class SummaryVersion(BaseModel):
    """A single version of an automatically generated or revised summary."""

    intake_id: str
    version: int = Field(..., ge=1, description="Version number for the summary")
    summary_text: str
    notes: Optional[str] = Field(
        default=None,
        description="Reviewer or clinician notes associated with the revision",
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp recording when this version was created",
    )
