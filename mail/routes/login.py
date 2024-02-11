from flask import render_template
from mail.core.locale import get_preferred_language, Strings


async def login():
    lang = get_preferred_language()
    strings = Strings(lang)

    return render_template("login.html", **{
        "title": "Willkommen bei Strawberry Mail",
        "strings": strings,
    })
