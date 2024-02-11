import hashlib

from flask import g

from mail.utils.colors import *
from mail.core.config import config
from mail.utils.hash import generate_hash

from email.header import decode_header
from email.utils import parsedate_to_datetime

import email
import imaplib
import socket


class ImapServerException(Exception):
    def __init__(self, message="Connection error"):
        self.message = message
        super().__init__(self.message)


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

    def test_connection(self):
        try:
            status, folder_list = self.connection.list()

            if status == 'OK':
                return True
            else:
                raise ImapServerException

        except:
            raise ImapServerException

    def login(self, username, password):
        self.connection.login(username, password)

    def logout(self):
        self.connection.logout()

    def list_mailboxes(self):
        status, mailboxes = self.connection.list()

        if status == "OK":
            return mailboxes

        return None


def get_imap():
    if 'imap' not in g:
        connection = ImapServer(config.imap_host, config.imap_port)

        g.imap = connection

    return g.imap


def get_all_emails(connection):
    try:
        status, messages = connection.select('INBOX')
        if status == 'OK':
            messages = int(messages[0])

            emails = []
            for i in range(messages, 0, -1):
                status, msg_data = connection.fetch(str(i), '(RFC822)')
                if status == 'OK':
                    msg = email.message_from_bytes(msg_data[0][1])
                    subject, subject_encoding = decode_header(msg['Subject'])[0]
                    sender, encoding = decode_header(msg.get('From'))[0]
                    date = parsedate_to_datetime(msg.get('Date')).strftime('%Y-%m-%d %H:%M:%S')

                    subject = subject.decode(subject_encoding or 'utf-8') if subject_encoding else subject
                    sender = sender.decode(encoding or 'utf-8') if encoding else sender

                    email_info = {
                        'id': generate_hash(i),
                        'subject': subject,
                        'sender': sender,
                        'date': date
                    }

                    emails.append(email_info)

        return emails

    except Exception as e:
        print(f"Error while getting email: {e}")
        return []


def get_email_by_id(email_id, connection):
    status, messages = connection.select('INBOX')

    status, message_data = connection.fetch(str(email_id), '(RFC822)')

    if status == 'OK':
        raw_email = message_data[0][1]
        msg = email.message_from_bytes(raw_email)

        sender, encoding = decode_header(msg.get('From'))[0]

        if isinstance(sender, bytes):
            sender = sender.decode(encoding or 'utf-8', 'ignore')

        subject, encoding = decode_header(msg.get('Subject'))[0]

        if isinstance(subject, bytes):
            subject = subject.decode(encoding or 'utf-8', 'ignore')

        receiver, encoding = decode_header(msg.get('To'))[0]

        if isinstance(receiver, bytes):
            receiver = receiver.decode(encoding or 'utf-8', 'ignore')

        date = msg.get('Date')

        content = ''
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == 'text/plain':
                    content = part.get_payload(decode=True).decode('utf-8', 'ignore')
                    break
        else:
            content = msg.get_payload(decode=True).decode('utf-8', 'ignore')

        return {
            'id': email_id,
            'sender': sender,
            'receiver': receiver,
            'subject': subject,
            'date': date,
            'content': content
        }
    else:
        return None