from flask import Flask

from mail.core.config import *
from mail.tools.utilities import load_secret

app = Flask(
    __name__,
    static_url_path=Config.static_url_path,
    static_folder=Config.static_folder,
    template_folder=Config.template_folder
)

app.config["SECRET_KEY"] = load_secret()

