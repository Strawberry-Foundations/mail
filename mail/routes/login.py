from flask import render_template


async def login():
    return render_template("login.html", **{
        "title": "Willkommen bei Strawberry Mail"
    })
