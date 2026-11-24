from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ChatRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    message: str = Field(min_length=1, max_length=2000)
    session_id: UUID | None = None


class ChatResponse(BaseModel):
    reply: str
    session_id: UUID
