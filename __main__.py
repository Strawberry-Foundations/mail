from mail.core.app import app
from mail.core.config import Config

if __name__ == "__main__":
    app.run(host=Config.address, port=Config.port, debug=Config.debug_mode, threaded=Config.threaded)
    