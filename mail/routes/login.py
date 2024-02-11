from flask import render_template, request


async def login():
    accept_language = request.headers.get('Accept-Language')

    return render_template("login.html", **{
        "title": "Willkommen bei Strawberry Mail",
        "lang": accept_language,
    })
