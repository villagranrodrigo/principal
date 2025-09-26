const form = document.getElementById("interview-form");
const previewEl = document.getElementById("preview");
const downloadBtn = document.getElementById("download-btn");
const copyBtn = document.getElementById("copy-btn");
const clearBtn = document.getElementById("clear-btn");

const formatDate = (rawDate) => {
  if (!rawDate) return "";
  try {
    const date = new Date(rawDate);
    return new Intl.DateTimeFormat("es-CL", {
      dateStyle: "long",
    }).format(date);
  } catch (error) {
    return rawDate;
  }
};

const buildText = (data) => {
  const lines = [
    `Paciente: ${data.paciente || ""}`,
    `Profesional: ${data.profesional || ""}`,
    `Fecha: ${formatDate(data.fecha)}`,
  ];

  if (data.tipo) {
    lines.push(`Tipo de entrevista: ${data.tipo}`);
  }

  lines.push("".padEnd(40, "-"));

  if (data.motivo) {
    lines.push("Motivo de consulta:");
    lines.push(data.motivo.trim());
    lines.push("");
  }

  if (data.resumen) {
    lines.push("Resumen / Hallazgos principales:");
    lines.push(data.resumen.trim());
    lines.push("");
  }

  if (data.proximos) {
    lines.push("Próximos pasos:");
    lines.push(data.proximos.trim());
  }

  lines.push("".padEnd(40, "-"));
  lines.push("Generado con Clinyco - Registro de entrevistas");

  return lines.join("\n");
};

let currentObjectUrl = null;

const syncPreview = () => {
  const formData = new FormData(form);
  const data = Object.fromEntries(formData.entries());
  const text = buildText(data);
  previewEl.value = text;

  const blob = new Blob([text], { type: "text/plain;charset=utf-8" });
  if (currentObjectUrl) {
    URL.revokeObjectURL(currentObjectUrl);
  }
  const fileNameParts = [
    "clinyco",
    data.paciente?.trim().replace(/\s+/g, "-") || "paciente",
    data.fecha || new Date().toISOString().slice(0, 10),
  ];
  const fileName = `${fileNameParts.join("_")}.txt`;
  currentObjectUrl = URL.createObjectURL(blob);
  downloadBtn.download = fileName;
  downloadBtn.href = currentObjectUrl;
};

form.addEventListener("input", syncPreview);
form.addEventListener("submit", (event) => {
  event.preventDefault();
  syncPreview();
  downloadBtn.click();
});

copyBtn.addEventListener("click", async () => {
  if (!previewEl.value) return;
  try {
    await navigator.clipboard.writeText(previewEl.value);
    copyBtn.textContent = "¡Copiado!";
    copyBtn.disabled = true;
    setTimeout(() => {
      copyBtn.textContent = "Copiar texto";
      copyBtn.disabled = false;
    }, 2000);
  } catch (error) {
    alert("No se pudo copiar el texto. Puedes copiarlo manualmente.");
  }
});

clearBtn.addEventListener("click", () => {
  form.reset();
  syncPreview();
  form.querySelector("input")?.focus();
});

syncPreview();

window.addEventListener("beforeunload", () => {
  if (currentObjectUrl) {
    URL.revokeObjectURL(currentObjectUrl);
  }
});
