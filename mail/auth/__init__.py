from flask import session, redirect
from functools import wraps
from mail.core.logger import logger


async def is_user_authenticated(email):
    if email == "julian@strawberryfoundations.xyz":
        return True
    else:
        return False


def require_login(view_func):
    @wraps(view_func)
    async def wrapper(*args, **kwargs):
        if '_strawberryid.email' not in session and 'auth.email' not in session:
            logger.log(f"Unknown user tried to access {view_func.__name__}")
            return redirect("/login")

        email = session.get("auth.email")

        if not await is_user_authenticated(email):
            logger.log(f"{email} (unknown email) tried to access {view_func.__name__}")
            return redirect("/login")

        return await view_func(*args, **kwargs)

    return wrapper


def require_not_logged_in(view_func):
    @wraps(view_func)
    async def wrapper(*args, **kwargs):
        if '_strawberryid.email' in session or 'auth.email' in session:
            return redirect("/dashboard")

        return await view_func(*args, **kwargs)

    return wrapper
