import re
import unicodedata
from uuid import UUID, uuid4

from fastapi import APIRouter

from app.api.schemas import ChatRequest, ChatResponse

router = APIRouter()

CATALOG_UNAVAILABLE_REPLY = (
    "Le catalogue des formations sera bientôt disponible. "
    "En attendant, vous pouvez me demander les conditions d’admission "
    "ou les étapes de préinscription."
)


def _normalize_message(message: str) -> str:
    normalized = unicodedata.normalize("NFKD", message)
    without_accents = "".join(
        character for character in normalized if not unicodedata.combining(character)
    )
    return re.sub(r"\s+", " ", without_accents.casefold()).strip()


def _build_reply(message: str) -> str:
    normalized = _normalize_message(message)

    if any(
        keyword in normalized
        for keyword in ("formation", "formations", "filiere", "filieres", "parcours")
    ):
        return CATALOG_UNAVAILABLE_REPLY

    if any(
        keyword in normalized
        for keyword in ("admission", "admis", "conditions", "condition", "dossier")
    ):
        return (
            "Les conditions d’admission dépendent de la formation choisie. "
            "Préparez vos diplômes, relevés de notes et pièces d’identité, "
            "puis vérifiez les exigences propres à votre parcours dès que le catalogue sera disponible."
        )

    if any(
        keyword in normalized
        for keyword in ("preinscription", "inscription", "candidature", "candidater")
    ):
        return (
            "La préinscription se fera en trois étapes : choisir une formation, "
            "renseigner vos informations et déposer les pièces demandées. "
            "La procédure détaillée sera disponible prochainement."
        )

    return (
        "Je peux vous renseigner sur les formations, les conditions d’admission "
        "et la procédure de préinscription. Pouvez-vous préciser votre question ?"
    )


@router.get("/health", tags=["health"])
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "smartcampus-api"}


@router.post("/chat", response_model=ChatResponse, tags=["chat"])
async def chat(request: ChatRequest) -> ChatResponse:
    session_id: UUID = request.session_id or uuid4()
    return ChatResponse(reply=_build_reply(request.message), session_id=session_id)
