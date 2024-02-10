from mail.core.app import App, app
from mail.core.config import Config

config = Config()
runtime = App(app)

if __name__ == "__main__":
    runtime.run(config)
