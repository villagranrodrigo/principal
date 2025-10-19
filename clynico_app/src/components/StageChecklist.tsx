import type { Stage } from '../types';

interface StageChecklistProps {
  stages: Stage[];
  completed: Record<number, boolean>;
  onToggleStage: (stageId: number, value: boolean) => void;
}

export function StageChecklist({ stages, completed, onToggleStage }: StageChecklistProps) {
  return (
    <section>
      <h3>Etapas del flujo</h3>
      <div className="stage-list">
        {stages.map((stage) => {
          const isCompleted = Boolean(completed[stage.id]);
          return (
            <article key={stage.id} className={`stage-card${isCompleted ? ' completed' : ''}`}>
              <h3>
                {stage.id.toString().padStart(2, '0')} — {stage.name}
              </h3>
              <p>{stage.description}</p>
              <label style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
                <input
                  type="checkbox"
                  checked={isCompleted}
                  onChange={(event) => onToggleStage(stage.id, event.target.checked)}
                />
                {isCompleted ? 'Completado' : 'Pendiente'}
              </label>
            </article>
          );
        })}
      </div>
    </section>
  );
}
