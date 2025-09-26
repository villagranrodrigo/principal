# Clinyco - Generador de entrevistas

Aplicación web sencilla en español para registrar la información obtenida en una entrevista clínica y generar automáticamente un archivo de texto descargable con el resumen.

## ¿Cómo usarla?

1. Abre `public/index.html` en tu navegador (puedes hacer doble click sobre el archivo o servirlo con cualquier servidor estático).
2. Completa los campos de la entrevista.
3. La vista previa mostrará el contenido del archivo de texto.
4. Pulsa **Generar archivo** para descargar el `.txt` o **Copiar texto** para tenerlo en el portapapeles.

Todos los datos se procesan en tu navegador, sin enviar información a servidores externos.

## Servir la aplicación localmente

Si prefieres usar un servidor estático, puedes hacerlo con `npx serve` (Node.js) desde la carpeta del proyecto:

```bash
npx serve public
```

Luego abre la URL indicada (por defecto http://localhost:3000) para ver la aplicación.
