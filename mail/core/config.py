from mail import server_dir
import yaml

with open(server_dir + "/config.yml", "r") as _config:
    config = yaml.load(_config, Loader=yaml.SafeLoader)


class Config:
    address = config["host"]["address"]
    port = config["host"]["port"]

    debug_mode = config["flags"]["debug_mode"]
    threaded = config["flags"]["threaded"]

    static_url_path = config["vars"]["static_url_path"]
    static_folder = config["vars"]["static_folder"]
    template_folder = config["vars"]["template_folder"]
