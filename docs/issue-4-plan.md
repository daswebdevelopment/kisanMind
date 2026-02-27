# Issue #4: Groq AI integration for WhatsApp queries

## Delivered
- Added Groq client integration in `backend/services/ai_service.py` using model `llama3-8b-8192`.
- Added agriculture-focused system prompt for Indian farming context.
- Updated webhook pipeline to:
  1. save incoming text query,
  2. request AI answer from Groq,
  3. update `Query.answer` in DB,
  4. send AI answer to farmer on WhatsApp.
- Added fallback message when Groq fails:
  - "Maafi kijiye, abhi technical samasya hai. Thodi der baad dobara try karein. 🙏"
- Added `groq` dependency and `GROQ_API_KEY` in backend env example.
