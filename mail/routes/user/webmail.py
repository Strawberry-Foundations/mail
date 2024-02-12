from flask import render_template, session

from mail.auth import require_login
from mail.core.logger import logger
from mail.core.locale import get_preferred_language, Strings
from mail.imap.client import get_imap, ImapServerException, get_all_emails, get_sent_emails
from mail.imap.mail import Email, MailBox


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

    email = Email(imap.connection)

    mailboxes = email.get_mailboxes()
    inbox_emails = email.fetch_mails(MailBox.INBOX)
    sent_emails = email.fetch_mails(MailBox.SENT)
    drafts_emails = email.fetch_mails(MailBox.DRAFTS)
    trash_emails = email.fetch_mails(MailBox.TRASH)
    flagged_emails = email.fetch_flagged_mail()

    return render_template("user/webmail.html", **{
        "mailboxes": mailboxes,
        "inbox_emails": inbox_emails,
        "sent_emails": sent_emails,
        "drafts_emails": drafts_emails,
        "trash_emails": trash_emails,
        "flagged_emails": flagged_emails,
        "strings": strings,
        "title": f"{strings.load('inbox')} - {session.get('auth.email')}",
        "user_mail": user_email,
    })
