from flask import redirect, request, session
from mail import STRAWBERRY_ID_URL
from mail.core.config import config
import requests


async def callback():
    redir_lang = request.args.get("hl", default="en")

    if "code" not in request.args:
        return redirect("/login?err=no_code")

    data = requests.get(f"{STRAWBERRY_ID_URL}api/callback?code={request.args['code']}").json()

    if data["data"]["status"] == "Invalid code":
        return redirect("/login?err=invalid_code")

    user_data = data["data"]["user"]

    email: str = user_data["email"]
    email_tld = email.split("@")[1]

    if not email_tld.rstrip() == config.mail_tld:
        return redirect("/login?err=not_permitted")

    session["_strawberryid.username"] = user_data["username"]
    session["_strawberryid.email"] = user_data["email"]
    session["_strawberryid.full_name"] = user_data["full_name"]
    session["_strawberryid.avatarurl"] = user_data["profile_picture_url"]

    return redirect("/login?sid_success")
