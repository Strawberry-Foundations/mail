from flask import render_template, session

from mail.auth import require_login
from mail.imap.client import get_imap, ImapServerException, get_all_emails


@require_login
async def dashboard():
    try:
        imap = get_imap().test_connection()

    except ImapServerException:
        user_email = session.get("auth.email")
        password = session.get("auth.password")

        imap = get_imap()
        imap.connect()
        imap.login(user_email, password)

    emails = get_all_emails(imap.connection)

    return render_template("user/dashboard.html", **{
        "emails": emails
    })
