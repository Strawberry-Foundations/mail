from mail.core.app import App, app

runtime = App(app)

if __name__ == "__main__":
    runtime.setup()
    runtime.run()
