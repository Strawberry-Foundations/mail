from flask import session, redirect
from functools import wraps

from mail.core.logger import logger
from mail.core.config import config

import imaplib


async def is_user_authenticated(email, password):
    mail = None

    try:
        mail = imaplib.IMAP4_SSL(config.imap_host, config.imap_port)
        mail.login(email, password)

        return True

    except Exception as e:
        return False

    finally:
        if 'mail' in locals():
            mail.logout()


def require_login(view_func):
    @wraps(view_func)
    async def wrapper(*args, **kwargs):
        if '_strawberryid.email' not in session and 'auth.email' not in session:
            logger.log(f"Unknown user tried to access {view_func.__name__}")
            return redirect("/login")

        email = session.get("auth.email")
        password = session.get("auth.password")

        if not await is_user_authenticated(email, password):
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
