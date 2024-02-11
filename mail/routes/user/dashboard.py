from flask import render_template, session
from email.header import decode_header

from mail.auth import require_login
from mail.imap.client import get_imap, ImapServerException

import email


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

    mbox = imap.list_mailboxes()

    imap.connection.select("inbox")

    status, messages = imap.connection.search(None, "ALL")
    mail_ids = messages[0].split()

    content = ""

    for mail_id in mail_ids:
        # Holen Sie sich die Roh-E-Mail-Daten
        status, msg_data = imap.connection.fetch(mail_id, "(RFC822)")
        raw_email = msg_data[0][1]

        # Analysiere die E-Mail
        msg = email.message_from_bytes(raw_email)
        subject, encoding = decode_header(msg["Subject"])[0]

        if isinstance(subject, bytes):
            subject = subject.decode(encoding or "utf-8")

        content_type, content_encoding = msg.get_content_type(), msg.get("Content-Transfer-Encoding")

        content = content + f"Subject: {subject}\nFrom: {msg['From']}\nDate: {msg['Date']}Body:\n"

        if content_type == "text/plain":
            body = msg.get_payload(decode=True)
            content = content + body.decode("utf-8")

        elif content_type == "text/html":
            body = msg.get_payload(decode=True)
            content = content + body.decode("utf-8")

        else:
            if msg.is_multipart():
                content_type = msg.get_content_type()
                content_disposition = str(msg.get("Content-Disposition"))

                if "attachment" not in content_disposition:
                    body = msg.get_payload(decode=True)
                    try:
                        content = content + body.decode("utf-8")
                    except:
                        try:
                            content = content + body
                        except:
                            pass

    return render_template("user/dashboard.html", **{
        "mbox": mbox,
        "content": content
    })
