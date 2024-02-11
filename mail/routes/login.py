import imaplib

from flask import render_template, request, redirect, session

from mail.core.locale import get_preferred_language, Strings
from mail.core.config import config
from mail.imap.client import get_imap_connection
from mail.core.logger import logger
from mail import STRAWBERRY_ID_URL


async def login():
    lang = get_preferred_language()
    strings = Strings(lang)
    redir_lang = "en"

    error = False
    error_msg = None

    if "strawberry_id_auth" in request.args:
        match lang:
            case "de-de":
                redir_lang = "de"
            case "en-us":
                redir_lang = "en"

        return redirect(f"{STRAWBERRY_ID_URL}{redir_lang}/login/?redirect=0.0.0.0:8080")

    if "sid_success" in request.args:
        email = session.get("_strawberryid.email")

        email_tld = email.split("@")[1]

        if not email_tld.rstrip() == config.mail_tld:
            return redirect("/login?err=not_permitted")

        session["auth.email"] = email

        return redirect("/dashboard")

    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        try:
            connection = get_imap_connection()
            connection.login(email, password)

            session["auth.email"] = email
            session["auth.password"] = password

            logger.log(f"{email} logged in")
            return redirect("/dashboard")

        except imaplib.IMAP4.error as err:
            logger.log(text=err)
            error = True
            error_msg = strings.load("invalid_credentials")

    return render_template("login.html", **{
        "title": strings.load("title_welcome"),
        "strings": strings,
        "error": error,
        "error_msg": error_msg,
    })
