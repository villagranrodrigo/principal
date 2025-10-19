# Clynico App

Aplicación web inicial para gestionar el seguimiento de pacientes bariátricos usando Firebase. Este paquete complementa la CLI `patient_tracking` y sirve como base para desplegar la solución en la consola de Firebase.

## Objetivos

- Registrar pacientes y consultar su estado general.
- Marcar el avance de las etapas del flujo bariátrico.
- Enviar mensajes transaccionales y registrar la conversación en Firestore.
- Preparar la integración con servicios externos (por ejemplo, Twilio o WhatsApp Business) desde Cloud Functions.

## Estructura del directorio

```
clynico_app/
├── firebase.json              # Configuración base para Hosting y Firestore.
├── firestore.rules            # Reglas mínimas de seguridad.
├── firestore.indexes.json     # Índices recomendados para consultas.
├── README.md                  # Este archivo.
├── package.json               # Dependencias de la SPA (Vite + React + TypeScript).
├── tsconfig.json              # Configuración de TypeScript para el cliente.
├── tsconfig.node.json         # Configuración de TypeScript para herramientas.
├── vite.config.ts             # Configuración de compilación.
└── src/
    ├── App.tsx                # Componente principal de la interfaz.
    ├── firebase.ts            # Inicialización del SDK de Firebase.
    ├── main.tsx               # Punto de entrada de la aplicación.
    ├── types.ts               # Tipos compartidos.
    ├── data/
    │   └── stages.ts          # Definición del flujo de etapas.
    ├── hooks/
    │   └── usePatients.ts     # Hook para manejar Firestore y pacientes.
    └── components/
        ├── MessageComposer.tsx
        ├── PatientDetails.tsx
        ├── PatientList.tsx
        └── StageChecklist.tsx
```

## Requisitos previos

1. **Node.js 18+** y **pnpm** o **npm**.
2. **Firebase CLI** (`npm install -g firebase-tools`).
3. Un proyecto en [Firebase Console](https://console.firebase.google.com/) con el nombre `clynicoapp` (o el que prefieras) y App Check habilitado.
4. Activar Firestore en modo producción.

## Pasos iniciales

1. Copia el repositorio o sincroniza los archivos en tu entorno de trabajo.
2. En la consola de Firebase, registra una aplicación Web (`</>`). Descarga la configuración y pégala en `src/firebase.ts`.
3. Instala las dependencias:

```bash
cd clynico_app
npm install
```

4. Ejecuta la aplicación en modo desarrollo:

```bash
npm run dev
```

5. Configura App Check desde la consola de Firebase, usando el proveedor reCAPTCHA v3 para la app Web. Copia la clave pública en `src/firebase.ts` dentro de `initializeAppCheck`.

6. Actualiza las reglas de seguridad ejecutando:

```bash
firebase deploy --only firestore:rules
```

> **Nota:** Antes de desplegar Hosting o Firestore asegúrate de ejecutar `firebase login` y de inicializar el directorio con `firebase use <tu-proyecto>`.

## Integración con Cloud Functions

- Ejecuta `firebase init functions` dentro de `clynico_app` si deseas agregar backend. Puedes usar TypeScript y agregar dependencias como `firebase-admin` y un SDK de mensajería.
- Define un trigger HTTP o Callable que reciba `patientId`, `subject`, `body` y `channel` y que guarde el mensaje en Firestore y envíe la notificación externa.
- Actualiza el hook `usePatients` para llamar a la Function cuando se envíen mensajes desde la interfaz.

## Estructura de colecciones sugerida

- `patients` (documentos con campos: `name`, `contact`, `preferredChannel`, `stageStatus`, `createdAt`, `updatedAt`).
- `patients/{patientId}/messages` para el historial de mensajes.
- `stages` (opcional) si deseas administrar dinámicamente las etapas desde Firestore.

## Próximos pasos

- Conectar autenticación con Google o correo/contraseña para el equipo clínico.
- Implementar control de acceso por roles con [Custom Claims](https://firebase.google.com/docs/auth/admin/custom-claims).
- Construir reportes usando BigQuery o Looker Studio conectados a Firestore.
- Automatizar mensajes recurrentes con Cloud Scheduler + Cloud Functions.

Este es un punto de partida modular. Puedes extenderlo con tus propias pantallas, integrar un diseño corporativo y añadir analítica con Google Analytics para Firebase.
