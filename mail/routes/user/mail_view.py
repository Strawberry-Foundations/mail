from flask import render_template, session, request

from mail.auth import require_login
from mail.imap.client import get_imap, ImapServerException
from mail.imap.mail import Email, MailBox


@require_login
async def mail_view(email_id, mailbox: str):
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

    email = Email(imap.connection)

    match mailbox.lower():
        case "inbox": mailbox = MailBox.INBOX
        case "sent": mailbox = MailBox.SENT
        case "drafts": mailbox = MailBox.DRAFTS
        case "trash": mailbox = MailBox.TRASH
        case "junk": mailbox = MailBox.JUNK

    mail_content = email.fetch_email(email_id, mailbox)

    if display_format == "json":
        return mail_content
