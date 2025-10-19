"""Workflow definition for seguimiento de pacientes bariátricos."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List


@dataclass(frozen=True)
class WorkflowStage:
    """Represents a single paso dentro del flujo de seguimiento."""

    id: int
    name: str
    description: str


STAGES: List[WorkflowStage] = [
    WorkflowStage(1, "Contacto inicial", "Registrar primer contacto con el paciente."),
    WorkflowStage(2, "Recordatorio 2-3 días", "Enviar recordatorio de seguimiento a los 2-3 días."),
    WorkflowStage(3, "Material informativo", "Compartir material informativo en PDF y enlaces útiles."),
    WorkflowStage(4, "Confirmar cita médica", "Confirmar la fecha y hora de la cita médica inicial."),
    WorkflowStage(5, "Resumen entrevista", "Enviar resumen de la entrevista o consulta médica."),
    WorkflowStage(6, "Evaluación cirujano", "Verificar si se completó la evaluación con el cirujano."),
    WorkflowStage(7, "Evaluación nutrióloga", "Verificar evaluación con la nutrióloga."),
    WorkflowStage(8, "Evaluación nutricionista", "Verificar evaluación con la nutricionista."),
    WorkflowStage(9, "Evaluación psicólogo", "Confirmar evaluación psicológica."),
    WorkflowStage(10, "Exámenes de sangre", "Revisar si se realizaron los exámenes de sangre."),
    WorkflowStage(11, "Endoscopia", "Confirmar endoscopia programada/completada."),
    WorkflowStage(12, "Ecografía", "Confirmar ecografía programada/completada."),
    WorkflowStage(13, "Revisión de exámenes", "Verificar revisión integral de exámenes."),
    WorkflowStage(14, "Agendamiento de cirugía", "Agendar la fecha definitiva de la cirugía."),
    WorkflowStage(15, "Indicaciones pre cirugía", "Enviar indicaciones y tips preoperatorios."),
    WorkflowStage(16, "Acompañamiento dieta pre", "Mensajes diarios de acompañamiento desde el día -5."),
    WorkflowStage(17, "Cirugía concretada", "Registrar que la cirugía fue realizada."),
    WorkflowStage(18, "Alta médica", "Confirmar el alta posterior a la cirugía."),
]


_STAGE_LOOKUP = {stage.id: stage for stage in STAGES}


def get_stage(stage_id: int) -> WorkflowStage:
    """Return a workflow stage by id."""
    try:
        return _STAGE_LOOKUP[stage_id]
    except KeyError as exc:
        raise ValueError(f"No existe etapa con id {stage_id}.") from exc


def iter_stages(stage_ids: Iterable[int] | None = None) -> Iterable[WorkflowStage]:
    """Iterar por etapas específicas o por todas."""
    if stage_ids is None:
        return iter(STAGES)
    return (_STAGE_LOOKUP[sid] for sid in stage_ids if sid in _STAGE_LOOKUP)
