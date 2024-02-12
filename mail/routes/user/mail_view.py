from flask import render_template, session, request

from mail.auth import require_login
from mail.imap.client import get_imap, ImapServerException
from mail.imap.mail import Email, MailBox
from mail.core.locale import get_preferred_language, Strings


@require_login
async def mail_view(email_id, mailbox: str):
    display_format = "web"
    lang = get_preferred_language()
    strings = Strings(lang)

    inbox_btn_css = ""
    drafts_btn_css = ""
    sent_btn_css = ""
    marked_btn_css = ""
    trash_btn_css = ""

    mailbox_str = ""

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
        case "inbox":
            mailbox = MailBox.INBOX
            inbox_btn_css = "sidebar--button-active"
            mailbox_str = strings.load("inbox")

        case "sent":
            mailbox = MailBox.SENT
            sent_btn_css = "sidebar--button-active"
            mailbox_str = strings.load("sent")

        case "drafts":
            mailbox = MailBox.DRAFTS
            drafts_btn_css = "sidebar--button-active"
            mailbox_str = strings.load("drafts")

        case "trash":
            mailbox = MailBox.TRASH
            trash_btn_css = "sidebar--button-active"
            mailbox_str = strings.load("trash")

        case "junk":
            mailbox = MailBox.JUNK

    mail_content = email.fetch_email(email_id, mailbox)

    if display_format == "json":
        return mail_content

    return render_template("user/mail_view.html", **{
        "strings": strings,
        "email": mail_content,
        "mailbox": mailbox_str,
        "rmailbox": mailbox.value.lower(),
        "inbox_btn_css": inbox_btn_css,
        "drafts_btn_css": drafts_btn_css,
        "sent_btn_css": sent_btn_css,
        "marked_btn_css": marked_btn_css,
        "trash_btn_css": trash_btn_css,
    })
