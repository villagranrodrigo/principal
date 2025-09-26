"""Patient summary orchestration pipeline."""
from __future__ import annotations

from typing import Dict, List, Optional

from .models import PatientIntakeData, SummaryVersion
from .store import SummaryStore
from .summarizer import BaseSummarizer


class PatientSummaryPipeline:
    """Coordinates summarization, storage, and analytics for patient intakes."""

    def __init__(self, summarizer: BaseSummarizer, store: Optional[SummaryStore] = None) -> None:
        self.summarizer = summarizer
        self.store = store or SummaryStore()

    def propose_summary(self, intake: PatientIntakeData) -> SummaryVersion:
        """Generate and persist a summary for the provided intake data."""

        summary_text = self.summarizer.summarize(intake)
        return self.store.add_version(intake=intake, summary_text=summary_text)

    def revise_summary(
        self,
        intake_id: str,
        notes: str,
        summary_text: Optional[str] = None,
    ) -> SummaryVersion:
        """Record a revised summary, optionally overriding the generated text."""

        latest = self.store.get_latest(intake_id)
        if latest is None:
            raise ValueError(f"No intake data found for '{intake_id}'")

        intake_data = self.store.get_intake_data(intake_id)
        assert intake_data is not None  # for type checkers

        new_summary_text = summary_text or latest.summary_text
        return self.store.add_version(intake=intake_data, summary_text=new_summary_text, notes=notes)

    def compare_versions(self, intake_id: str) -> List[Dict[str, object]]:
        """Produce diffs between consecutive summary versions for the intake."""

        import difflib

        versions = self.store.get_versions(intake_id)
        diffs: List[Dict[str, object]] = []
        for previous, current in zip(versions, versions[1:]):
            diff = "\n".join(
                difflib.unified_diff(
                    previous.summary_text.splitlines(),
                    current.summary_text.splitlines(),
                    fromfile=f"version {previous.version}",
                    tofile=f"version {current.version}",
                    lineterm="",
                )
            )
            diffs.append(
                {
                    "from_version": previous.version,
                    "to_version": current.version,
                    "diff": diff,
                }
            )
        return diffs

    def collect_training_corpus(self) -> List[Dict[str, object]]:
        """Collect summaries and intake data for model fine-tuning."""

        corpus: List[Dict[str, object]] = []
        for intake_id, record in self.store.iter_all():
            corpus.append(
                {
                    "intake_id": intake_id,
                    "version": record.version,
                    "summary_text": record.summary_text,
                    "notes": record.notes,
                    "intake_data": record.intake_data.dict(),
                }
            )
        return corpus
