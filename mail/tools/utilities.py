from mail import server_dir

def load_secret():
    with open(server_dir + "/secret.key", "r") as _secret:
        return _secret.read()