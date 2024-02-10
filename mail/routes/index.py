from mail.core.app import app


@app.route("/")
async def index():
    return "Hello, World"
