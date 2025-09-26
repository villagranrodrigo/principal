"""In-memory persistence for patient summary versions."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Iterable, List, Optional

from .models import PatientIntakeData, SummaryVersion


@dataclass
class _StoredSummary:
    """Internal representation of a stored summary version."""

    version: int
    summary_text: str
    notes: Optional[str]
    created_at: datetime
    intake_data: PatientIntakeData

    def to_model(self, intake_id: str) -> SummaryVersion:
        return SummaryVersion(
            intake_id=intake_id,
            version=self.version,
            summary_text=self.summary_text,
            notes=self.notes,
            created_at=self.created_at,
        )


class SummaryStore:
    """Simple in-memory store for patient summary versions."""

    def __init__(self) -> None:
        self._store: Dict[str, List[_StoredSummary]] = {}

    def add_version(
        self,
        intake: PatientIntakeData,
        summary_text: str,
        notes: Optional[str] = None,
    ) -> SummaryVersion:
        versions = self._store.setdefault(intake.intake_id, [])
        version_number = len(versions) + 1
        record = _StoredSummary(
            version=version_number,
            summary_text=summary_text,
            notes=notes,
            created_at=datetime.utcnow(),
            intake_data=intake,
        )
        versions.append(record)
        return record.to_model(intake.intake_id)

    def get_versions(self, intake_id: str) -> List[SummaryVersion]:
        return [record.to_model(intake_id) for record in self._store.get(intake_id, [])]

    def get_latest(self, intake_id: str) -> Optional[_StoredSummary]:
        versions = self._store.get(intake_id)
        if not versions:
            return None
        return versions[-1]

    def iter_all(self) -> Iterable[tuple[str, _StoredSummary]]:
        for intake_id, versions in self._store.items():
            for record in versions:
                yield intake_id, record

    def has_intake(self, intake_id: str) -> bool:
        return intake_id in self._store

    def get_intake_data(self, intake_id: str) -> Optional[PatientIntakeData]:
        versions = self._store.get(intake_id)
        if not versions:
            return None
        return versions[0].intake_data
