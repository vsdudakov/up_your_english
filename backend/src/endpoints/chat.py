import uuid

from fastapi import APIRouter, Depends

from src.endpoints.deps import get_service, get_session_id
from src.schemas.chat import MessageSchema
from src.services.chat import ChatService

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)


@router.post("/message")
async def post_message(
    payload: MessageSchema,
    session_id: uuid.UUID = Depends(get_session_id),
    chat_service: ChatService = Depends(get_service(ChatService)),
) -> MessageSchema:
    return await chat_service.handle_message(
        session_id,
        payload,
    )
