from flask import render_template, session, request

from mail.auth import require_login
from mail.imap.client import get_imap, ImapServerException, get_email_by_id
from mail.utils.hash import generate_hash


@require_login
async def inbox(email_id):
    display_format = "web"

    if "format" in request.args:
        display_format = request.args.get("format")

    try:
        imap = get_imap().test_connection()

    except ImapServerException:
        user_email = session.get("auth.email")
        password = session.get("auth.password")

        imap = get_imap()
        imap.connect()
        imap.login(user_email, password)

    email = get_email_by_id(email_id, imap.connection)

    if display_format == "json":
        return email
