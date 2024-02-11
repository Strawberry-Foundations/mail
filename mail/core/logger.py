from mail.utils.colors import *
from datetime import datetime
from enum import Enum


class LogType(Enum):
    UserManager = f"[{BLUE}{BOLD}UManager{CRESET}]    "


class Logger:
    def __init__(self):
        self.logger = self

    def log(self, text, log_type: LogType = LogType.UserManager):
        timestamp_string = datetime.now().strftime("%d/%b/%Y %H:%M:%S")

        print(f"{log_type.value}[{GREEN}{timestamp_string}{CRESET}] {text}")


logger = Logger()
