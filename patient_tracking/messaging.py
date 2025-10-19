"""Herramientas de mensajería simuladas para seguimiento de pacientes."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List


class MessagingChannel(str, Enum):
    """Canales soportados para contactar al paciente."""

    CHAT = "chat"
    SMS = "sms"


@dataclass
class MessageRecord:
    """Mensaje que fue enviado a un paciente."""

    patient_id: str
    subject: str
    body: str
    channel: MessagingChannel
    sent_at: str

    @classmethod
    def create(cls, patient_id: str, subject: str, body: str, channel: MessagingChannel) -> "MessageRecord":
        return cls(
            patient_id=patient_id,
            subject=subject,
            body=body,
            channel=channel,
            sent_at=datetime.utcnow().isoformat(timespec="seconds"),
        )


class MessagingService:
    """Servicio simple que registra mensajes en memoria o almacenamiento externo."""

    def __init__(self, storage: "StorageProtocol") -> None:
        self._storage = storage

    def send_message(self, patient_id: str, subject: str, body: str, channel: MessagingChannel) -> MessageRecord:
        """Enviar (simulado) un mensaje y guardarlo en el historial."""
        record = MessageRecord.create(patient_id, subject, body, channel)
        self._storage.save_message(record)
        return record


class StorageProtocol:
    """Protocol interface for typing. Avoids runtime dependency on typing_extensions."""

    def save_message(self, message: MessageRecord) -> None:  # pragma: no cover - interface
        raise NotImplementedError


class InMemoryStorage(StorageProtocol):
    """Implementación simple en memoria, útil para pruebas."""

    def __init__(self) -> None:
        self.messages: List[MessageRecord] = []

    def save_message(self, message: MessageRecord) -> None:
        self.messages.append(message)


