"""Summarization utilities for the patient summary pipeline."""
from __future__ import annotations

from abc import ABC, abstractmethod
from textwrap import dedent

from .models import PatientIntakeData


class BaseSummarizer(ABC):
    """Interface for classes capable of summarizing patient intake data."""

    @abstractmethod
    def summarize(self, intake: PatientIntakeData) -> str:
        """Generate a textual summary for the provided intake data."""


class TemplateSummarizer(BaseSummarizer):
    """A deterministic summarizer that formats intake data into a template."""

    def summarize(self, intake: PatientIntakeData) -> str:
        history = intake.history.strip() or "No additional history provided."
        medications = intake.medications.strip() or "No medications reported."
        template = f"""
        Patient {intake.patient_name} (age {intake.age}) presents with {intake.chief_complaint}.
        History: {history}
        Medications: {medications}
        """
        return dedent(template).strip()
