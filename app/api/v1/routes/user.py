from fastapi import APIRouter, BackgroundTasks, Depends, Security, HTTPException, status
from pydantic import EmailStr
import logging

from app.config import config
from app.database.dependencies import sessDep
from app.functions.emailer import send_email
from app.models.auth.functions import authorize_and_load
from app.models.auth.role import Role
from app.models.auth.token import Token
from app.models.user import User
from app.models.user.schemas import PasswordsIn, UserOut, UserIn

router = APIRouter(prefix="/user", tags=["User"])

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(
    *,
    async_session: sessDep,
    user_in: UserIn,
    send_email: bool = True,
    bt: BackgroundTasks
):
    try:
        if await User.find(async_session=async_session, email=user_in.email, raise_=False):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
        user = await User(**user_in.model_dump()).save(async_session)
        if send_email:
            await request_reset_password(async_session, email=user.email, bt=bt)
        return user
    except HTTPException as e:
        logger.error(f"Registration failed: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error during registration: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.get("/me", response_model=UserOut, status_code=200)
async def me(user: User = Depends(authorize_and_load)):
    return user


@router.get("/request-reset-password/{email}", status_code=200)
async def request_reset_password(
    async_session: sessDep, email: EmailStr, bt: BackgroundTasks
) -> dict:
    user = await User.find(async_session, raise_=True, email=email)
    token = (
        Token(
            id=user.id,  # type: ignore
            scope=[Role.RESET],
            expires_in=config.RESET_EXPIRE_SECONDS,
        )
        .encode()
        .access_token
    )
    if config.ENV_STATE == "test":
        return {"message": token}
    content = f"Use the following token/link to reset your password: {token}"
    subject = "Reset Password"
    bt.add_task(send_email, email=email, subject=subject, content=content)
    return {"message": f"Reset password email sent to {email}"}


@router.post("/reset-password", status_code=200, response_model=UserOut)
async def reset_password(
    async_session: sessDep,
    passwords: PasswordsIn,
    user: User = Security(authorize_and_load, scopes=[Role.RESET]),
    token: str | None = None,  # noqa: F841
):
    user = await User.get(
        async_session, id=user.id
    )  # sessDep not cached when using Security Scopes
    return await user.update(
        async_session, verified=True, password=passwords.password.get_secret_value()
    )
