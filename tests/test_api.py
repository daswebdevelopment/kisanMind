from pathlib import Path
import unittest


class TestIssueSkeleton(unittest.TestCase):
    def test_issue_one_files_still_exist(self) -> None:
        self.assertTrue(Path('frontend/src/views/Home.vue').exists())
        self.assertTrue(Path('backend/routes/health.py').exists())

    def test_issue_two_model_files_exist(self) -> None:
        for file_path in [
            'backend/models/farmer.py',
            'backend/models/query.py',
            'backend/models/crop.py',
            'backend/schemas/farmer.py',
            'backend/schemas/query.py',
            'backend/schemas/crop.py',
        ]:
            self.assertTrue(Path(file_path).exists(), msg=f'Missing {file_path}')

    def test_issue_three_webhook_files_exist(self) -> None:
        self.assertTrue(Path('backend/routes/webhook.py').exists())
        self.assertTrue(Path('backend/services/whatsapp.py').exists())

    def test_issue_four_ai_service_exists(self) -> None:
        ai_content = Path('backend/services/ai_service.py').read_text(encoding='utf-8')
        self.assertIn('from groq import Groq', ai_content)
        self.assertIn('MODEL_NAME = "llama3-8b-8192"', ai_content)
        self.assertIn('SYSTEM_PROMPT', ai_content)
        self.assertIn('max_tokens=500', ai_content)
        self.assertIn('temperature=0.7', ai_content)

    def test_query_answer_nullable_for_ai_pipeline(self) -> None:
        model_content = Path('backend/models/query.py').read_text(encoding='utf-8')
        schema_content = Path('backend/schemas/query.py').read_text(encoding='utf-8')
        self.assertIn('answer: Mapped[str | None]', model_content)
        self.assertIn('answer: str | None = None', schema_content)

    def test_health_route_includes_database_status(self) -> None:
        content = Path('backend/routes/health.py').read_text(encoding='utf-8')
        self.assertIn('"database": db_status', content)
        self.assertIn('SELECT 1', content)

    def test_startup_creates_tables(self) -> None:
        content = Path('backend/main.py').read_text(encoding='utf-8')
        self.assertIn('Base.metadata.create_all', content)
        self.assertIn('app.include_router(webhook_router)', content)

    def test_webhook_issue_four_flow_present(self) -> None:
        content = Path('backend/routes/webhook.py').read_text(encoding='utf-8')
        self.assertIn('@router.get("/whatsapp")', content)
        self.assertIn('@router.post("/whatsapp")', content)
        self.assertIn('if message.get("type") != "text"', content)
        self.assertIn('answer = generate_farmer_answer(text)', content)
        self.assertIn('query.answer = answer', content)
        self.assertIn('send_whatsapp_message(phone_number, answer)', content)
        self.assertIn('FALLBACK_MESSAGE', content)
        self.assertIn('return {"status": "received"}', content)

    def test_env_contains_keys(self) -> None:
        env_content = Path('.env.example').read_text(encoding='utf-8')
        backend_env_content = Path('backend/.env.example').read_text(encoding='utf-8')
        for key in ['WHATSAPP_TOKEN=', 'WHATSAPP_PHONE_ID=', 'WHATSAPP_VERIFY_TOKEN=', 'GROQ_API_KEY=']:
            self.assertIn(key, env_content)
        self.assertIn('GROQ_API_KEY=', backend_env_content)

    def test_requirements_include_groq(self) -> None:
        req = Path('backend/requirements.txt').read_text(encoding='utf-8')
        self.assertIn('groq', req)


if __name__ == '__main__':
    unittest.main()
