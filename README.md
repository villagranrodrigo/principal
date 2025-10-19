# Seguimiento de pacientes bariátricos

Aplicación de línea de comandos para gestionar el flujo de comunicación con pacientes candidatos a cirugía bariátrica. Permite registrar pacientes, enviar mensajes (chat o SMS simulados), marcar el avance de cada etapa del proceso y consultar el historial de interacciones.

## Requisitos

- Python 3.11 o superior.

## Instalación

No se requieren dependencias adicionales. Puede ejecutarse directamente con `python` usando la ruta del paquete.

```bash
python -m patient_tracking --help
```

## Flujo de etapas

El flujo contemplado incluye:

1. Contacto inicial.
2. Recordatorio a los 2-3 días.
3. Envío de material informativo.
4. Confirmación de cita médica.
5. Envío del resumen de la entrevista médica.
6. Verificación de evaluación con cirujano.
7. Verificación de evaluación con nutrióloga.
8. Verificación de evaluación con nutricionista.
9. Evaluación psicológica.
10. Exámenes de sangre.
11. Endoscopia.
12. Ecografía.
13. Revisión de exámenes.
14. Agendamiento de cirugía.
15. Envío de indicaciones previas a la cirugía.
16. Mensajes de acompañamiento en dieta pre cirugía (día a día desde el quinto día previo).
17. Confirmación de cirugía concretada.
18. Alta médica.

## Uso básico

Registrar o actualizar un paciente:

```bash
python -m patient_tracking registrar P001 "Ana López" "+34 600 123 456" --channel sms
```

Listar pacientes registrados:

```bash
python -m patient_tracking listar
```

Marcar etapas como completas o pendientes:

```bash
# Marcar la etapa 6 (evaluación con cirujano) como completada
python -m patient_tracking marcar P001 6

# Marcar la misma etapa como pendiente
python -m patient_tracking marcar P001 6 --pendiente
```

Enviar mensajes utilizando plantillas:

```bash
python -m patient_tracking enviar P001 --template recordatorio
python -m patient_tracking enviar P001 --template confirmar_cita --param appointment_date="12/04 10:00"
```

Enviar mensajes personalizados:

```bash
python -m patient_tracking enviar P001 --subject "Recordatorio de análisis" --body "Hola Ana, recuerda asistir a tus exámenes de sangre mañana." --channel chat
```

Consultar historial y flujo completo:

```bash
python -m patient_tracking historial P001
python -m patient_tracking flujo
```

Los mensajes se almacenan en `data/patients.json`, que puede respaldarse o compartirse con el equipo clínico según sea necesario.

## Aplicación web Clynico

En el directorio `clynico_app/` encontrarás una aplicación web creada con Vite + React + TypeScript preparada para desplegarse en Firebase Hosting. Incluye:

- Configuración inicial de Firebase (`firebase.json`, reglas e índices de Firestore).
- Un cliente que consume Firestore para listar pacientes, marcar etapas y enviar mensajes.
- Hook reutilizable `usePatients` para gestionar el estado compartido.
- Componentes base listos para personalizar con la identidad visual de Clynico.

Para comenzar:

1. Copia `.env.example` a `.env` y añade las credenciales de tu proyecto Firebase y la clave pública de App Check.
2. Instala dependencias con `npm install` dentro de `clynico_app/`.
3. Ejecuta `npm run dev` para desarrollar localmente y `npm run build` para generar la versión de producción.
4. Implementa autenticación y funciones de mensajería según los requerimientos del flujo clínico.

Consulta `clynico_app/README.md` para instrucciones detalladas de configuración y despliegue.
