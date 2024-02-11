from flask import g

from mail.utils.colors import *
from mail.core.config import config

import imaplib
import socket


def get_imap_connection():
    if 'imap_connection' not in g:
        connection = imaplib.IMAP4_SSL(config.imap_host, config.imap_port)
        g.imap_connection = connection

    return g.imap_connection


class ImapServer:
    def __init__(self, host: str, port: int):
        self.connection = None
        self.host = host
        self.port = port

    def connect(self):
        try:
            print(f"{YELLOW}{BOLD} ! Connecting to IMAP Server {self.host}:{self.port}...{CRESET}")
            self.connection = imaplib.IMAP4_SSL(self.host, self.port)
            print(f"{GREEN}{BOLD} ✓ Connected{CRESET}")

        except (ConnectionRefusedError, socket.gaierror) as err:
            print(f"{RED}{BOLD} × Could not connect to IMAP Server {self.host}:{self.port}{CRESET}")
            print(f"{RED}{BOLD} ↳ {err}")
            exit(1)

        return self.connection

    def login(self, username, password):
        self.connection.login(username, password)

    def logout(self):
        self.connection.logout()

    def list_mailboxes(self):
        status, mailboxes = self.connection.list()

        if status == "OK":
            return mailboxes

        return None
