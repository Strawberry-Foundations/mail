from flask import redirect, request
from mail import STRAWBERRY_ID_URL
from mail.core.app import config

import requests


async def callback():
    redir_lang = request.args.get("hl", default="en")

    if "code" not in request.args:
        return redirect("/login")

    data = requests.get(f"{STRAWBERRY_ID_URL}api/callback?code={request.args['code']}").json()

    status = data["data"]["status"]

    print(status)

    if status == "Invalid code":
        return redirect("/login")

    user_data = data["data"]["user"]

    email: str = user_data["email"]

    email_tld = email.split("@")[1]

    print(email)
    print(email_tld)
