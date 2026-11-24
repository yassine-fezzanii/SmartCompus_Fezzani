import unittest
from uuid import UUID

from app.api.routes import _build_reply
from app.api.schemas import ChatRequest


class ChatBehaviorTests(unittest.TestCase):
    def test_training_question_reports_unavailable_catalog(self) -> None:
        self.assertIn("catalogue", _build_reply("Quelles formations sont disponibles ?"))

    def test_admission_question_returns_admission_guidance(self) -> None:
        self.assertIn("conditions d’admission", _build_reply("Quelles sont les conditions d'admission ?"))

    def test_pre_registration_question_returns_procedure(self) -> None:
        self.assertIn("trois étapes", _build_reply("Comment fonctionne la préinscription ?"))

    def test_unknown_question_returns_clarification(self) -> None:
        self.assertIn("Pouvez-vous préciser", _build_reply("Quel temps fera-t-il demain ?"))

    def test_session_id_is_optional_and_validated(self) -> None:
        generated = ChatRequest(message="Bonjour", session_id=None)
        provided = ChatRequest(message="Bonjour", session_id="123e4567-e89b-12d3-a456-426614174000")
        self.assertIsNone(generated.session_id)
        self.assertEqual(provided.session_id, UUID("123e4567-e89b-12d3-a456-426614174000"))


if __name__ == "__main__":
    unittest.main()
