"""Plantillas de mensajes reutilizables."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class MessageTemplate:
    slug: str
    subject: str
    body: str


TEMPLATES: Dict[str, MessageTemplate] = {
    "contacto_inicial": MessageTemplate(
        slug="contacto_inicial",
        subject="¡Bienvenido al programa de seguimiento!",
        body=(
            "Hola {name}, soy parte del equipo de acompañamiento. "
            "Gracias por tu interés, este es tu punto de contacto para todo el proceso."
        ),
    ),
    "recordatorio": MessageTemplate(
        slug="recordatorio",
        subject="Seguimiento programado",
        body=(
            "Hola {name}, ¿cómo te sientes? Te recordamos que estamos aquí para resolver tus dudas "
            "y acompañarte antes de tu primera cita."
        ),
    ),
    "material_informativo": MessageTemplate(
        slug="material_informativo",
        subject="Material informativo preoperatorio",
        body=(
            "Hola {name}, te comparto el material informativo: {material_links}. "
            "Por favor revísalo antes de nuestra próxima conversación."
        ),
    ),
    "confirmar_cita": MessageTemplate(
        slug="confirmar_cita",
        subject="Confirmación de cita médica",
        body=(
            "Hola {name}, confirmamos tu cita el {appointment_date}. "
            "Si necesitas reprogramar avísanos con anticipación."
        ),
    ),
    "resumen_entrevista": MessageTemplate(
        slug="resumen_entrevista",
        subject="Resumen de la entrevista",
        body=(
            "Hola {name}, aquí tienes el resumen de lo conversado: {interview_summary}. "
            "Cualquier comentario es bienvenido."
        ),
    ),
    "indicaciones_pre": MessageTemplate(
        slug="indicaciones_pre",
        subject="Indicaciones previas a la cirugía",
        body=(
            "Hola {name}, recuerda seguir estas indicaciones antes de la cirugía: {pre_surgery_tips}."
        ),
    ),
    "acompanamiento_pre": MessageTemplate(
        slug="acompanamiento_pre",
        subject="Día {day_offset} de la dieta pre cirugía",
        body=(
            "Hola {name}, ¡ya queda poco! Para hoy te recomendamos: {daily_tip}. Sigue las instrucciones "
            "y avísanos si necesitas apoyo."
        ),
    ),
}


def render_template(slug: str, **kwargs: str) -> MessageTemplate:
    template = TEMPLATES.get(slug)
    if not template:
        raise KeyError(f"No existe la plantilla '{slug}'.")
    return MessageTemplate(
        slug=template.slug,
        subject=template.subject.format(**kwargs),
        body=template.body.format(**kwargs),
    )
