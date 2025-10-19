import type { Stage } from '../types';

export const STAGES: Stage[] = [
  { id: 1, name: 'Contacto inicial', description: 'Primer acercamiento con el paciente.' },
  { id: 2, name: 'Recordatorio', description: 'Mensaje de recordatorio a los 2-3 días.' },
  { id: 3, name: 'Material informativo', description: 'Enviar PDF y enlaces informativos.' },
  { id: 4, name: 'Confirmar cita médica', description: 'Confirmar la primera cita con el equipo médico.' },
  { id: 5, name: 'Resumen entrevista', description: 'Compartir el resumen de la entrevista médica.' },
  { id: 6, name: 'Evaluación cirujano', description: 'Validar que se realizó la evaluación con el cirujano.' },
  { id: 7, name: 'Evaluación nutrióloga', description: 'Confirmar la valoración con la nutrióloga.' },
  { id: 8, name: 'Evaluación nutricionista', description: 'Revisar la cita con el nutricionista.' },
  { id: 9, name: 'Evaluación psicólogo', description: 'Verificar evaluación psicológica.' },
  { id: 10, name: 'Exámenes de sangre', description: 'Confirmar entrega de exámenes de laboratorio.' },
  { id: 11, name: 'Endoscopia', description: 'Comprobar realización de endoscopia.' },
  { id: 12, name: 'Ecografía', description: 'Validar ecografía previa.' },
  { id: 13, name: 'Revisión de exámenes', description: 'Revisión global de estudios.' },
  { id: 14, name: 'Agendar cirugía', description: 'Definir fecha de cirugía.' },
  { id: 15, name: 'Indicaciones preoperatorias', description: 'Enviar indicaciones y tips previos a cirugía.' },
  { id: 16, name: 'Dieta pre cirugía', description: 'Mensajes diarios desde 5 días antes de la cirugía.' },
  { id: 17, name: 'Cirugía realizada', description: 'Confirmar que la cirugía se concretó.' },
  { id: 18, name: 'Alta médica', description: 'Registrar el alta del paciente.' }
];
