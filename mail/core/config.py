from mail import server_dir
import yaml

with open(server_dir + "/config.yml", "r") as _config:
    config = yaml.load(_config, Loader=yaml.SafeLoader)

static_url_path = config["vars"]["static_url_path"]
static_folder = config["vars"]["static_folder"]
template_folder = config["vars"]["template_folder"]


class Config:
    def __init__(self):
        self.address = config["host"]["address"]
        self.port = config["host"]["port"]

        self.debug_mode = config["flags"]["debug_mode"]
        self.threaded = config["flags"]["threaded"]
