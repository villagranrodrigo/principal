import { useEffect } from 'react';
import { usePatients } from './hooks/usePatients';
import { PatientList } from './components/PatientList';
import { PatientDetails } from './components/PatientDetails';
import { StageChecklist } from './components/StageChecklist';
import { MessageComposer } from './components/MessageComposer';
import { STAGES } from './data/stages';

function EmptyState() {
  return (
    <div>
      <h2>Selecciona un paciente</h2>
      <p>Registra pacientes desde el panel lateral para comenzar su seguimiento.</p>
    </div>
  );
}

export default function App() {
  const { patients, loading, selectPatient, selectedPatient, messages, addPatient, toggleStage, sendMessage } = usePatients();

  useEffect(() => {
    if (!selectedPatient && patients.length > 0) {
      selectPatient(patients[0].id);
    }
  }, [patients, selectedPatient, selectPatient]);

  return (
    <div className="app-shell">
      <PatientList
        patients={patients}
        selectedPatientId={selectedPatient?.id ?? null}
        onSelect={selectPatient}
        onAddPatient={addPatient}
      />
      <main className="content">
        {loading && <p>Cargando pacientes…</p>}
        {!loading && !selectedPatient && <EmptyState />}
        {selectedPatient && (
          <div>
            <PatientDetails patient={selectedPatient} messages={messages} />
            <StageChecklist stages={STAGES} completed={selectedPatient.stageStatus} onToggleStage={toggleStage} />
            <MessageComposer
              defaultChannel={selectedPatient.preferredChannel}
              onSend={sendMessage}
              disabled={loading}
            />
          </div>
        )}
      </main>
    </div>
  );
}
