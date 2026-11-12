# LogPulse 📊

LogPulse is a full-stack application log analyzer and alert dashboard built with **FastAPI**, **SQLAlchemy**, **Pydantic**, and **Tailwind CSS**.

## Features
- 🚀 **Service Registry**: Register and monitor multiple applications across production, staging, and development environments.
- 📋 **Log Ingestion & Filtering**: Real-time log ingestion supporting `INFO`, `WARNING`, `ERROR`, and `FATAL` severity levels with instant level/module filtering.
- 📈 **Error Analytics**: Automated calculation of aggregate log counts and error rate percentages.
- ⚡ **Modern Responsive UI**: Dark-themed observability single-page dashboard built with Tailwind CSS.

---

## Setup & Running (Ubuntu WSL)

1. **Create and activate virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate