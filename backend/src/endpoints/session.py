import uuid

from fastapi import APIRouter, HTTPException, Request, Response

from src.schemas.session import CreateSessionSchema, EFunctionality, EModel, SessionSchema

router = APIRouter(
    prefix="/session",
    tags=["session"],
)


@router.post("")
async def post_session(
    response: Response,
    payload: CreateSessionSchema,
) -> SessionSchema:
    session_id = uuid.uuid4()
    response.set_cookie(key="model", value=payload.model.value, httponly=True)
    response.set_cookie(key="functionality", value=payload.functionality.value, httponly=True)
    if payload.style:
        response.set_cookie(key="style", value=payload.style, httponly=True)
    response.set_cookie(key="session_id", value=str(session_id), httponly=True)
    return SessionSchema(
        session_id=session_id,
        model=payload.model,
        functionality=payload.functionality,
    )


@router.get("")
async def get_session(
    request: Request,
) -> SessionSchema:
    session_id = request.cookies.get("session_id")
    model = request.cookies.get("model")
    functionality = request.cookies.get("functionality")
    style = request.cookies.get("style")
    if not session_id or not model or not functionality:
        raise HTTPException(status_code=401, detail="Session not found.")
    return SessionSchema(
        session_id=uuid.UUID(session_id),
        model=EModel(model),
        functionality=EFunctionality(functionality),
        style=style,
    )
