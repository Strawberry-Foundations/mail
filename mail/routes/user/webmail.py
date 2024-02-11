from flask import render_template, session

from mail.auth import require_login
from mail.core.logger import logger
from mail.core.locale import get_preferred_language, Strings
from mail.imap.client import get_imap, ImapServerException, get_all_emails


@require_login
async def webmail():
    lang = get_preferred_language()
    strings = Strings(lang)

    user_email = session.get("auth.email")
    password = session.get("auth.password")

    try:
        imap = get_imap().test_connection()

    except ImapServerException as err:
        logger.log(err)
        imap = get_imap()
        imap.connect()
        imap.login(user_email, password)

    emails = get_all_emails(imap.connection)

    return render_template("user/webmail.html", **{
        "emails": emails,
        "strings": strings,
        "title": f"{strings.load('inbox')} - {session.get('auth.email')}",
        "user_mail": user_email,
    })
