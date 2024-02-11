from mail.core.app import App, app, config

runtime = App(app)

if __name__ == "__main__":
    runtime.run(config)
