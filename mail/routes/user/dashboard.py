from flask import render_template, session
from mail.auth import require_login
from mail.core.mail import imap


@require_login
async def dashboard():
    return render_template("user/dashboard.html")
