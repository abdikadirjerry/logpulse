# LogPulse 📊

LogPulse is an application log analyzer and alert dashboard built with FastAPI, SQLAlchemy, and Tailwind CSS.

## Features
- **Log Ingestion Engine**: Ingest structured server logs (INFO, WARNING, ERROR, FATAL).
- **Error Analytics**: Track error frequencies and time-series distributions.
- **Alert Rules**: Configure threshold-based alerts for recurring server errors.

## Setup & Running
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload