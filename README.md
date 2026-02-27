# KisanMind

Base project skeleton for KisanMind with:
- **Frontend:** Vue 3 + Vite
- **Backend:** FastAPI + SQLAlchemy (PostgreSQL) + Groq (Llama 3)

## Project Structure

```text
kisanmind/
├── frontend/
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models/
│   │   ├── base.py
│   │   ├── farmer.py
│   │   ├── query.py
│   │   └── crop.py
│   ├── schemas/
│   │   ├── farmer.py
│   │   ├── query.py
│   │   └── crop.py
│   ├── routes/
│   │   ├── health.py
│   │   └── webhook.py
│   ├── services/
│   │   ├── ai_service.py
│   │   └── whatsapp.py
│   └── requirements.txt
├── .env.example
└── README.md
```

## Backend (FastAPI)

### Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
cp .env.example .env
```

### Run

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### Endpoints

- `GET /health` → returns API and database status
- `GET /webhook/whatsapp` → Meta webhook verification endpoint
- `POST /webhook/whatsapp` → receives incoming WhatsApp messages, gets Groq AI answer, stores answer in DB, and sends answer back

## Frontend (Vue 3 + Vite)

### Setup

```bash
cd frontend
npm install
```

### Run

```bash
npm run dev
```

The Home view calls the backend `/health` endpoint and displays **"KisanMind API is running"** when healthy.

## Environment Variables

`.env.example` contains required placeholders:
- `API_URL`
- `GROQ_API_KEY`
- `BHASHINI_API_KEY`
- `AGMARKNET_API_KEY`
- `DATABASE_URL`
- `WHATSAPP_TOKEN`
- `WHATSAPP_PHONE_ID`
- `WHATSAPP_VERIFY_TOKEN`
