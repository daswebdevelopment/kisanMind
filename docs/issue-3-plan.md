# Issue #3: WhatsApp webhook receive, log, and acknowledge

## Delivered
- Added webhook routes in `backend/routes/webhook.py`:
  - `GET /webhook/whatsapp` for Meta verification.
  - `POST /webhook/whatsapp` for inbound message processing.
- Added WhatsApp send utility in `backend/services/whatsapp.py` using Meta Cloud API.
- Inbound text message flow now:
  1. Extracts sender phone and text.
  2. Auto-creates `Farmer` if not found.
  3. Saves message to `Query` with `answer=None`.
  4. Sends acknowledgement reply.
- Route always returns HTTP 200 payload (`{"status": "received"}`) for POST.
- Added WhatsApp env variables to root and backend env examples.
