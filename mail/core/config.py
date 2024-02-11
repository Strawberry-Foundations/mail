from mail import server_dir
import yaml

with open(server_dir + "/config.yml", "r") as _config:
    config_data = yaml.load(_config, Loader=yaml.SafeLoader)

static_url_path = config_data["vars"]["static_url_path"]
static_folder = config_data["vars"]["static_folder"]
template_folder = config_data["vars"]["template_folder"]


class Config:
    def __init__(self):
        self.address = config_data["host"]["address"]
        self.port = config_data["host"]["port"]

        self.debug_mode = config_data["flags"]["debug_mode"]
        self.threaded = config_data["flags"]["threaded"]

        self.mail_tld = config_data["vars"]["mail_tld"]
        self.static_url_path = config_data["vars"]["static_url_path"]
        self.static_folder = config_data["vars"]["static_folder"]
        self.template_folder = config_data["vars"]["template_folder"]

config = Config()
