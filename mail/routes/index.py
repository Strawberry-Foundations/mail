from flask import redirect


async def index():
    return redirect("/dashboard")
