from mail.utils.colors import *
from datetime import datetime


class Logger:
    def __init__(self):
        self.logger = self

    def log(self, text):
        timestamp_string = datetime.now().strftime("%d/%b/%Y %H:%M:%S")

        print(f"[{GREEN}{timestamp_string}{CRESET}] {text}")


logger = Logger()
