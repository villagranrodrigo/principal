# Principal Patient Summary Service

This project exposes a small FastAPI application that can generate, revise, and
inspect patient intake summaries. It uses a deterministic template-based
summarizer and an in-memory store to keep track of each revision.

## Getting started

1. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Launch the API server:

   ```bash
   uvicorn app.api:app --reload
   ```

   The service listens on `http://127.0.0.1:8000` by default. Interactive API
documentation is available at `/docs`.

## Available endpoints

| Method & Path | Description |
| --- | --- |
| `POST /summaries/propose` | Accepts `PatientIntakeData` JSON and returns a generated `SummaryVersion`. |
| `POST /summaries/{intake_id}/revise` | Records a revision, storing clinician notes and optional updated summary text. |
| `GET /summaries/{intake_id}/diffs` | Provides unified diffs between consecutive summary versions. |
| `GET /corpus` | Exposes the stored corpus for model training or audit workflows. |

## Data contracts

### PatientIntakeData

```json
{
  "intake_id": "unique-string",
  "patient_name": "Ada Lovelace",
  "age": 36,
  "chief_complaint": "Headache",
  "history": "Optional historical context",
  "medications": "Optional medication list"
}
```

### SummaryRevisionRequest

```json
{
  "intake_id": "unique-string",
  "notes": "Clinician notes explaining the revision",
  "summary_text": "Optional updated summary text"
}
```

The `/corpus` endpoint returns an array of objects combining intake data,
summary text, and notes for every stored version, making it suitable for
collecting training data for downstream models.
