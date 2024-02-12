from mail import server_dir
import re


def load_secret():
    with open(server_dir + "/secret.key", "r") as _secret:
        return _secret.read()


def extract_name_from_email(email_address):
    match = re.search(r'^(.*?)\s*<', email_address)
    return match.group(1).strip() if match else email_address
