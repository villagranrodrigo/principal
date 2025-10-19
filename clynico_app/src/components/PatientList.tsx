import type { Patient } from '../types';

interface PatientListProps {
  patients: Patient[];
  selectedPatientId: string | null;
  onSelect: (patientId: string) => void;
  onAddPatient: () => void;
}

export function PatientList({ patients, selectedPatientId, onSelect, onAddPatient }: PatientListProps) {
  return (
    <aside className="sidebar">
      <h1>Clynico</h1>
      <p>Seguimiento integral de pacientes bariátricos.</p>
      <button className="primary" onClick={onAddPatient} style={{ width: '100%', marginTop: '1rem' }}>
        + Registrar paciente
      </button>
      <ul className="patient-list">
        {patients.map((patient) => (
          <li key={patient.id}>
            <button
              className={`patient-button${selectedPatientId === patient.id ? ' active' : ''}`}
              onClick={() => onSelect(patient.id)}
              type="button"
            >
              <strong>{patient.name}</strong>
              <br />
              <small>{patient.contact}</small>
            </button>
          </li>
        ))}
      </ul>
    </aside>
  );
}
