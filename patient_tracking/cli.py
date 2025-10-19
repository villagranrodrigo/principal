"""Interfaz de línea de comandos para el seguimiento de pacientes."""
from __future__ import annotations

import argparse
import json
from typing import Dict, Iterable

from .messaging import MessagingChannel, MessagingService
from .storage import PatientStorage, ensure_patient
from .templates import TEMPLATES, render_template
from .workflow import STAGES, get_stage


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Herramienta simple para hacer seguimiento de pacientes bariátricos",
    )
    parser.add_argument(
        "--storage",
        default="data/patients.json",
        help="Ruta al archivo JSON donde se guardará la información.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    register = subparsers.add_parser("registrar", help="Registrar o actualizar un paciente")
    register.add_argument("patient_id", help="Identificador único, por ejemplo el número de expediente")
    register.add_argument("name", help="Nombre completo del paciente")
    register.add_argument("contact", help="Datos de contacto (teléfono, email, etc.)")
    register.add_argument(
        "--channel",
        choices=[channel.value for channel in MessagingChannel],
        default=MessagingChannel.CHAT.value,
        help="Canal preferido para los mensajes",
    )

    list_parser = subparsers.add_parser("listar", help="Listar pacientes registrados")

    show_parser = subparsers.add_parser("ver", help="Ver detalle de un paciente")
    show_parser.add_argument("patient_id")

    stage_parser = subparsers.add_parser("marcar", help="Marcar una etapa como completa o pendiente")
    stage_parser.add_argument("patient_id")
    stage_parser.add_argument("stage_id", type=int)
    stage_parser.add_argument(
        "--pendiente",
        action="store_true",
        help="Marcar la etapa como pendiente en lugar de completada",
    )

    workflow_parser = subparsers.add_parser("flujo", help="Mostrar todas las etapas del proceso")

    send_parser = subparsers.add_parser("enviar", help="Enviar un mensaje al paciente")
    send_parser.add_argument("patient_id")
    send_parser.add_argument(
        "--channel",
        choices=[channel.value for channel in MessagingChannel],
        help="Canal a utilizar (por defecto el preferido del paciente)",
    )
    send_parser.add_argument("--subject", help="Asunto del mensaje")
    send_parser.add_argument("--body", help="Cuerpo del mensaje")
    send_parser.add_argument(
        "--template",
        choices=sorted(TEMPLATES.keys()),
        help="Usar una plantilla predefinida",
    )
    send_parser.add_argument(
        "--param",
        action="append",
        default=[],
        help="Parámetros para la plantilla en formato clave=valor",
    )

    history_parser = subparsers.add_parser("historial", help="Ver historial de mensajes")
    history_parser.add_argument("patient_id")

    return parser


def parse_params(pairs: Iterable[str]) -> Dict[str, str]:
    params: Dict[str, str] = {}
    for pair in pairs:
        if "=" not in pair:
            raise ValueError(f"El parámetro '{pair}' no tiene el formato clave=valor")
        key, value = pair.split("=", 1)
        params[key] = value
    return params


def handle_register(args: argparse.Namespace, storage: PatientStorage) -> None:
    patient = ensure_patient(storage, args.patient_id, args.name, args.contact, args.channel)
    print(f"Paciente {patient.patient_id} registrado/actualizado correctamente.")


def handle_list(storage: PatientStorage) -> None:
    patients = storage.list_patients()
    if not patients:
        print("No hay pacientes registrados.")
        return
    for patient in patients:
        completed = len(patient.completed_stages())
        pending = len(patient.pending_stages())
        print(
            f"- {patient.patient_id}: {patient.name} | Contacto: {patient.contact} | "
            f"Canal: {patient.preferred_channel.value} | Etapas completadas: {completed} | Pendientes: {pending}"
        )


def handle_show(args: argparse.Namespace, storage: PatientStorage) -> None:
    patient = storage.get_patient(args.patient_id)
    if not patient:
        print("Paciente no encontrado.")
        return
    print(json.dumps(patient.to_dict(), indent=2, ensure_ascii=False))


def handle_stage(args: argparse.Namespace, storage: PatientStorage) -> None:
    patient = storage.get_patient(args.patient_id)
    if not patient:
        print("Paciente no encontrado.")
        return
    try:
        stage = get_stage(args.stage_id)
    except ValueError as exc:
        print(str(exc))
        return
    completed = not args.pendiente
    patient.mark_stage(stage.id, completed)
    storage.save_patient(patient)
    estado = "completada" if completed else "pendiente"
    print(f"Etapa '{stage.name}' marcada como {estado} para {patient.name}.")


def handle_workflow() -> None:
    for stage in STAGES:
        print(f"{stage.id:02d}. {stage.name} - {stage.description}")


def handle_send(args: argparse.Namespace, storage: PatientStorage) -> None:
    patient = storage.get_patient(args.patient_id)
    if not patient:
        print("Paciente no encontrado.")
        return

    channel_value = args.channel or patient.preferred_channel.value
    channel = MessagingChannel(channel_value)

    if args.template:
        try:
            params = parse_params(args.param)
            params.setdefault("name", patient.name)
            template = render_template(args.template, **params)
        except Exception as exc:  # pylint: disable=broad-except
            print(f"Error al usar la plantilla: {exc}")
            return
        subject = template.subject
        body = template.body
    else:
        if not args.subject or not args.body:
            print("Debe proporcionar --subject y --body si no usa una plantilla.")
            return
        subject = args.subject
        body = args.body

    messaging = MessagingService(storage)
    message = messaging.send_message(patient.patient_id, subject, body, channel)
    print(
        "Mensaje enviado:",
        json.dumps(
            {
                "patient_id": message.patient_id,
                "subject": message.subject,
                "body": message.body,
                "channel": message.channel.value,
                "sent_at": message.sent_at,
            },
            indent=2,
            ensure_ascii=False,
        ),
    )


def handle_history(args: argparse.Namespace, storage: PatientStorage) -> None:
    patient = storage.get_patient(args.patient_id)
    if not patient:
        print("Paciente no encontrado.")
        return
    if not patient.messages:
        print("No hay mensajes registrados para este paciente.")
        return
    for message in patient.messages:
        print(
            f"[{message.sent_at}] {message.channel.value.upper()} | {message.subject}\n{message.body}\n"
        )


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    storage = PatientStorage(args.storage)

    if args.command == "registrar":
        handle_register(args, storage)
    elif args.command == "listar":
        handle_list(storage)
    elif args.command == "ver":
        handle_show(args, storage)
    elif args.command == "marcar":
        handle_stage(args, storage)
    elif args.command == "flujo":
        handle_workflow()
    elif args.command == "enviar":
        handle_send(args, storage)
    elif args.command == "historial":
        handle_history(args, storage)
    else:  # pragma: no cover - safety net
        parser.print_help()


if __name__ == "__main__":  # pragma: no cover
    main()
