from flask import Flask

from mail.core.config import *
from mail.tools.utilities import load_secret

from mail.routes.index import index


app = Flask(
    __name__,
    static_url_path=Config.static_url_path,
    static_folder=Config.static_folder,
    template_folder=Config.template_folder
)

app.config["SECRET_KEY"] = load_secret()

app.add_url_rule("/", view_func=index)
