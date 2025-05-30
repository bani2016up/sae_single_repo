from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer

from ..config.cfg import DEV_MODE
from ..models.token import TokenPayload
from ..models.users import (
    UserLogin,
    UserRegister,
    PasswordResetRequest,
    AuthTokens,
    UserCredentialsChangeRequest,
)
from ..services.services import (
    delete_all_cookies,
    login,
    logout,
    register,
    verify_token,
    send_password_reset,
    login_with_password_reset,
    change_email,
    change_password,
)

auth_router = APIRouter()
security = HTTPBearer()


@auth_router.post("/users")
async def sign_up(user: UserRegister, request: Request):
    """
    Register a new user in the system (supabase auth & database user creation).

    Args:
        user (UserRegister): The user registration data including email and password.
        request (Request): The HTTP request object containing session information.

    Returns:
        UserRegisterResponse: A response model containing a success message and the user ID.
    """
    return await register(user, request.state.sess)


@auth_router.post("/sessions")
async def sign_in(user: UserLogin):
    """
    Authenticate a user and create a new session with cookies set.

    Args:
        user (UserLogin): The user login data including email and password.

    Returns:
        JSONResponse: A response containing a success message and authentication cookies set.
    """
    return await login(user)


@auth_router.delete("/sessions/")
async def sign_out(payload: TokenPayload = Depends(verify_token)):
    """
    Log out the authenticated user and clear session cookies.

    Args:
        payload (TokenPayload): The token payload containing user information, obtained from the access token.

    Returns:
        JSONResponse: A response confirming the user has been logged out, with cookies cleared.
    """
    return await logout(payload)


@auth_router.get("/users/me")
async def get_current_user(payload: TokenPayload = Depends(verify_token)):
    """
    Retrieve information about the currently authenticated user.

    Args:
        payload (TokenPayload): The token payload containing user information, obtained from the access token.

    Returns:
        TokenPayload: The payload containing the authenticated user's details.
    """
    return payload


@auth_router.post("/sessions/password-reset/request")
async def send_reset_link(user: PasswordResetRequest):
    """
    Send a password reset link to the user's email.

    Args:
        user (PasswordResetRequest): The request data containing the user's email.

    Returns:
        PasswordResetResponse: A response confirming that the password reset link has been sent.
    """
    return await send_password_reset(user)


@auth_router.post("/sessions/password-reset/login")
async def login_through_password_reset(tokens: AuthTokens):
    """
    Log in a user using tokens obtained from a password reset.

    Args:
        tokens (AuthTokens): The authentication tokens obtained from the password reset process.

    Returns:
        JSONResponse: A response confirming the user has been logged in, with new authentication cookies set.
    """
    return await login_with_password_reset(tokens)


@auth_router.post("/update-password")
async def update_password(
    credentials: UserCredentialsChangeRequest,
    payload: TokenPayload = Depends(verify_token),
):
    """
    Update the password for the authenticated user.

    Args:
        credentials (UserCredentialsChangeRequest): The request data containing the new password.
        payload (TokenPayload): The token payload containing user information, obtained from the access token.

    Returns:
        CredentialsResponse: A response confirming the password has been updated.
    """
    return await change_password(payload, credentials)


@auth_router.post("/update-email")
async def update_email(
    credentials: UserCredentialsChangeRequest,
    payload: TokenPayload = Depends(verify_token),
):
    """
    Update the email address for the authenticated user.

    Args:
        credentials (UserCredentialsChangeRequest): The request data containing the new email.
        payload (TokenPayload): The token payload containing user information, obtained from the access token.

    Returns:
        CredentialsResponse: A response confirming the email has been updated.
    """
    return await change_email(payload, credentials)


if DEV_MODE:

    @auth_router.delete("/delete_all_acookies")
    async def delete_auth_cookies():
        """
        Delete all authentication cookies (development mode only).

        Returns:
            JSONResponse: A response confirming that authentication cookies have been deleted.
        """
        return await delete_all_cookies()
