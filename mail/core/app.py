from flask import Flask

from mail.core.config import *
from mail.utils.utilities import load_secret
from mail.utils.colors import *

from mail.routes.index import index

import os

app = Flask(
    __name__,
    static_url_path=static_url_path,
    static_folder=static_folder,
    template_folder=template_folder
)

app.config["SECRET_KEY"] = load_secret()

app.add_url_rule("/", view_func=index)


class App:
    def __init__(self, flask_app: Flask):
        self.app = flask_app

    def run(self, app_config: Config):
        if not app_config.debug_mode:
            combined_path = os.path.join(self.app.root_path, self.app.template_folder)
            absolute_path = os.path.abspath(combined_path)

            print(f"   {GREEN}{BOLD}{UNDERLINE}Thanks for using Strawberry Mail Server!{CRESET}")
            print(f"   {BLUE}{BOLD}Root Path:{CRESET} {self.app.root_path}")
            print(f"   {BLUE}{BOLD}Template Path:{CRESET} {absolute_path}")

            print("")

        self.app.run(
            host=app_config.address,
            port=app_config.port,
            debug=app_config.debug_mode,
            threaded=app_config.threaded
        )
