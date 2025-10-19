# Guía de configuración Firebase para Clynico

Esta guía describe los pasos para crear la aplicación **Clynico** en Firebase Console, habilitar App Check y preparar los servicios necesarios.

## 1. Crear el proyecto

1. Ingresa a [Firebase Console](https://console.firebase.google.com/).
2. Haz clic en **Agregar proyecto** y asigna un nombre (por ejemplo, `clynicoapp`).
3. Desactiva Google Analytics si aún no vas a utilizarlo o configúralo según tus necesidades.
4. Espera a que Firebase aprovisione los recursos.

## 2. Registrar la aplicación Web

1. Dentro del proyecto, selecciona el ícono `</>` para añadir una nueva app Web.
2. Asigna un apodo (por ejemplo, `clynico-web`).
3. Marca la opción **Configurar Firebase Hosting** si planeas desplegar la SPA desde aquí.
4. Copia la configuración (`firebaseConfig`) que aparece al finalizar; la necesitarás en `clynico_app/src/firebase.ts` o en `.env`.

## 3. Habilitar App Check

1. En el menú lateral, ve a **App Check**.
2. Selecciona tu app Web y elige **Proveedor reCAPTCHA v3**.
3. Sigue las instrucciones para generar la clave pública y privada.
4. Coloca la clave pública en la variable `VITE_RECAPTCHA_KEY` del archivo `.env`.
5. Si lo deseas, habilita **Enforcement** para obligar a que todas las solicitudes incluyan el token de App Check.

## 4. Configurar Firestore

1. Entra a **Firestore Database** y pulsa **Crear base de datos**.
2. Selecciona el modo **Producción** y elige la región más cercana a tus usuarios.
3. Crea la colección `patients` con un documento de prueba para validar la conexión.
4. Organiza los subcolecciones `messages` según la estructura recomendada.

### Reglas de seguridad

Publica las reglas iniciales incluidas en `clynico_app/firestore.rules`:

```bash
cd clynico_app
firebase deploy --only firestore:rules
```

Posteriormente, ajusta las reglas para restringir la escritura únicamente a usuarios autenticados y con claims específicos.

### Índices

Despliega los índices recomendados:

```bash
firebase deploy --only firestore:indexes
```

## 5. Autenticación (opcional pero recomendado)

1. Habilita el proveedor **Correo/Contraseña** o **Google** desde **Authentication** → **Método de inicio de sesión**.
2. Configura reglas adicionales en Firestore que dependan de `request.auth.token.role` para diferenciar médicos, nutriólogos, etc.

## 6. Configurar herramientas locales

1. Instala Firebase CLI: `npm install -g firebase-tools`.
2. Ejecuta `firebase login` para vincular tu cuenta.
3. Desde el directorio `clynico_app`, ejecuta `firebase init` y selecciona Hosting, Firestore y (opcionalmente) Functions.
4. Asocia el proyecto remoto con `firebase use <ID_DEL_PROYECTO>`.

## 7. Despliegue inicial

1. Compila la aplicación: `npm run build`.
2. Previsualiza localmente: `firebase emulators:start` para probar reglas y seguridad.
3. Despliega a Hosting: `firebase deploy --only hosting`.

## 8. Próximos pasos

- Implementar Cloud Functions que envíen SMS o mensajes de WhatsApp usando proveedores externos.
- Configurar Cloud Scheduler para recordatorios automáticos.
- Integrar App Distribution o Crashlytics si desarrollas una versión móvil.
- Conectar BigQuery para analítica avanzada.

Siguiendo estos pasos tendrás la base de Clynico en Firebase, lista para iterar con el equipo clínico.
