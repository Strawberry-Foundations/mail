from flask import Flask

from mail.core.config import *
from mail.utils.utilities import load_secret

from mail.routes.index import index


app = Flask(
    __name__,
    static_url_path=Config.static_url_path,
    static_folder=Config.static_folder,
    template_folder=Config.template_folder
)

app.config["SECRET_KEY"] = load_secret()

app.add_url_rule("/", view_func=index)


class App:
    def __init__(self, flask_app: Flask):
        self.app = flask_app

    def setup(self):
        print("   Thanks for using Strawberry Mail Server!")
        print(f"   Root Path: {self.app.root_path}")

        print("")

    def run(self):
        self.app.run(host=Config.address, port=Config.port, debug=Config.debug_mode, threaded=Config.threaded)