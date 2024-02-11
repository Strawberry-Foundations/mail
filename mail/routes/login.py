from flask import render_template, request, redirect
from mail.core.locale import get_preferred_language, Strings
from mail import STRAWBERRY_ID_URL
import requests


async def login():
    lang = get_preferred_language()
    strings = Strings(lang)
    redir_lang = "en"

    if "strawberry_id_auth" in request.args:
        match lang:
            case "de-DE":
                redir_lang = "de"
            case "en-US":
                redir_lang = "en"

        return redirect(f"{STRAWBERRY_ID_URL}{redir_lang}/login/?redirect=0.0.0.0:8080")

    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

    return render_template("login.html", **{
        "title": strings.load("title_welcome"),
        "strings": strings,
    })
