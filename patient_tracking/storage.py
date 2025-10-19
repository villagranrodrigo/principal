"""Persistencia básica en archivos JSON para el seguimiento de pacientes."""
from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Dict, List, Optional

from .messaging import MessageRecord, MessagingChannel
from .workflow import STAGES


@dataclass
class Patient:
    """Representa la información clave del paciente."""

    patient_id: str
    name: str
    contact: str
    preferred_channel: MessagingChannel = MessagingChannel.CHAT
    notes: str = ""
    stage_status: Dict[str, bool] = field(default_factory=dict)
    messages: List[MessageRecord] = field(default_factory=list)

    def mark_stage(self, stage_id: int, completed: bool = True) -> None:
        self.stage_status[str(stage_id)] = completed

    def to_dict(self) -> Dict:
        return {
            "patient_id": self.patient_id,
            "name": self.name,
            "contact": self.contact,
            "preferred_channel": self.preferred_channel.value,
            "notes": self.notes,
            "stage_status": self.stage_status,
            "messages": [asdict(message) for message in self.messages],
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "Patient":
        patient = cls(
            patient_id=data["patient_id"],
            name=data["name"],
            contact=data["contact"],
            preferred_channel=MessagingChannel(data.get("preferred_channel", "chat")),
            notes=data.get("notes", ""),
        )
        patient.stage_status = data.get("stage_status", {})
        patient.messages = [
            MessageRecord(
                patient_id=msg["patient_id"],
                subject=msg["subject"],
                body=msg["body"],
                channel=MessagingChannel(msg["channel"]),
                sent_at=msg["sent_at"],
            )
            for msg in data.get("messages", [])
        ]
        return patient

    def completed_stages(self) -> List[int]:
        return [int(stage_id) for stage_id, completed in self.stage_status.items() if completed]

    def pending_stages(self) -> List[int]:
        completed = set(self.completed_stages())
        return [stage.id for stage in STAGES if stage.id not in completed]


class PatientStorage:
    """Wrapper sobre un archivo JSON para persistencia sencilla."""

    def __init__(self, path: str | Path = "data/patients.json") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self._write({"patients": {}})

    def _read(self) -> Dict:
        with self.path.open("r", encoding="utf-8") as fp:
            return json.load(fp)

    def _write(self, data: Dict) -> None:
        with self.path.open("w", encoding="utf-8") as fp:
            json.dump(data, fp, indent=2, ensure_ascii=False)

    def list_patients(self) -> List[Patient]:
        data = self._read()
        return [Patient.from_dict(payload) for payload in data.get("patients", {}).values()]

    def get_patient(self, patient_id: str) -> Optional[Patient]:
        data = self._read()
        payload = data.get("patients", {}).get(patient_id)
        if payload is None:
            return None
        return Patient.from_dict(payload)

    def save_patient(self, patient: Patient) -> None:
        data = self._read()
        patients = data.setdefault("patients", {})
        patients[patient.patient_id] = patient.to_dict()
        self._write(data)

    def save_message(self, message: MessageRecord) -> None:
        data = self._read()
        patients = data.setdefault("patients", {})
        payload = patients.get(message.patient_id)
        if not payload:
            raise ValueError(f"Paciente {message.patient_id} no existe.")
        payload.setdefault("messages", []).append(asdict(message))
        self._write(data)


def ensure_patient(storage: PatientStorage, patient_id: str, name: str, contact: str, channel: str) -> Patient:
    """Crea o actualiza un paciente asegurando que exista."""
    patient = storage.get_patient(patient_id)
    if patient is None:
        patient = Patient(
            patient_id=patient_id,
            name=name,
            contact=contact,
            preferred_channel=MessagingChannel(channel),
        )
    else:
        patient.name = name
        patient.contact = contact
        patient.preferred_channel = MessagingChannel(channel)
    storage.save_patient(patient)
    return patient
