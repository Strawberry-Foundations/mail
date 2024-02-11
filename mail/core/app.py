from flask import Flask

from mail.core.config import *
from mail.utils.utilities import load_secret
from mail.utils.colors import *

from mail.routes.index import index
from mail.routes.login import login
from mail.routes.api.callback import callback

import os

app = Flask(
    __name__,
    static_url_path=static_url_path,
    static_folder=static_folder,
    template_folder=template_folder
)

app.config["SECRET_KEY"] = load_secret()

app.add_url_rule("/", view_func=index)
app.add_url_rule("/login", view_func=login, methods={"GET", "POST"})
app.add_url_rule("/callback", view_func=callback)

config = Config()


class App:
    def __init__(self, flask_app: Flask):
        self.app = flask_app

    def run(self, app_config: Config):
        if not app_config.debug_mode:
            template_absolute = os.path.abspath(os.path.join(self.app.root_path, self.app.template_folder))
            static_absolute = os.path.abspath(os.path.join(self.app.root_path, self.app.static_folder))

            print(f"   {GREEN}{BOLD}{UNDERLINE}Thanks for using Strawberry Mail Server!{CRESET}")
            print(f"   {BLUE}{BOLD}Server Path:{CRESET} {server_dir}")
            print(f"   {BLUE}{BOLD}Root Path:{CRESET} {self.app.root_path}")
            print(f"   {BLUE}{BOLD}Template Path:{CRESET} {template_absolute}")
            print(f"   {BLUE}{BOLD}Static Path:{CRESET} {static_absolute}")

            print("")

        self.app.run(
            host=app_config.address,
            port=app_config.port,
            debug=app_config.debug_mode,
            threaded=app_config.threaded
        )
