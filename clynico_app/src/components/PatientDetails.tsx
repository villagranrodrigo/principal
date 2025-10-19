import type { Patient, PatientMessage } from '../types';

interface PatientDetailsProps {
  patient: Patient;
  messages: PatientMessage[];
}

export function PatientDetails({ patient, messages }: PatientDetailsProps) {
  return (
    <section>
      <header className="section-title">
        <div>
          <h2>{patient.name}</h2>
          <p>{patient.contact}</p>
        </div>
        <span className="badge">{patient.preferredChannel.toUpperCase()}</span>
      </header>
      <p>
        Paciente registrado el {patient.createdAt ? new Date(patient.createdAt).toLocaleString() : '—'}. Última
        actualización: {patient.updatedAt ? new Date(patient.updatedAt).toLocaleString() : '—'}.
      </p>
      <div>
        <h3>Historial de mensajes</h3>
        {messages.length === 0 && <p>No hay mensajes registrados.</p>}
        <ul>
          {messages.map((message) => (
            <li key={message.id}>
              <strong>
                [{new Date(message.sentAt).toLocaleString()}] {message.channel.toUpperCase()} — {message.subject}
              </strong>
              <p>{message.body}</p>
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}
