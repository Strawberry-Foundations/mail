from flask import render_template
from mail.auth import require_login


@require_login
async def dashboard():
    return render_template("user/dashboard.html")
