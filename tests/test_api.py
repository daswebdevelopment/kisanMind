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

    def test_health_route_includes_database_status(self) -> None:
        content = Path('backend/routes/health.py').read_text(encoding='utf-8')
        self.assertIn('"database": db_status', content)
        self.assertIn('SELECT 1', content)

    def test_startup_creates_tables(self) -> None:
        content = Path('backend/main.py').read_text(encoding='utf-8')
        self.assertIn('Base.metadata.create_all', content)
        self.assertIn('app.include_router(webhook_router)', content)

    def test_webhook_behaviors_present(self) -> None:
        content = Path('backend/routes/webhook.py').read_text(encoding='utf-8')
        self.assertIn('@router.get("/whatsapp")', content)
        self.assertIn('@router.post("/whatsapp")', content)
        self.assertIn('send_whatsapp_message(phone_number, ACK_MESSAGE)', content)
        self.assertIn('return {"status": "received"}', content)
        self.assertIn('if message.get("type") != "text"', content)

    def test_env_contains_whatsapp_keys(self) -> None:
        env_content = Path('.env.example').read_text(encoding='utf-8')
        self.assertIn('WHATSAPP_TOKEN=', env_content)
        self.assertIn('WHATSAPP_PHONE_ID=', env_content)
        self.assertIn('WHATSAPP_VERIFY_TOKEN=', env_content)


if __name__ == '__main__':
    unittest.main()
