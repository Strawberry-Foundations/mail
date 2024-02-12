from mail.utils.utilities import extract_name_from_email
from mail.core.logger import logger
from mail.err.imap import *

from email.utils import parsedate_to_datetime
from email import message_from_bytes
from email.header import decode_header

from datetime import datetime, date
from imaplib import IMAP4_SSL
from enum import Enum


class MailBox(Enum):
    INBOX = "INBOX"
    SENT = "Sent"
    DRAFTS = "Drafts"
    TRASH = "Trash"
    JUNK = "Junks"


class Email:
    def __init__(self, connection: IMAP4_SSL):
        self.connection = connection

    def fetch_mails(self, folder: MailBox):
        try:
            status, messages = self.connection.select(folder.value)

            if status == "OK":
                messages = int(messages[0])
                emails = []

                for i in range(messages, 0, -1):
                    status, msg_data = self.connection.fetch(str(i), '(RFC822)')

                    if status == "OK":
                        msg = message_from_bytes(msg_data[0][1])

                        subject, subject_encoding = decode_header(msg['Subject'])[0]
                        sender, sender_encoding = decode_header(msg.get('From'))[0]
                        receiver, sender_encoding = decode_header(msg.get('To'))[0]

                        mail_date = parsedate_to_datetime(msg.get('Date')).strftime('%Y-%m-%d %H:%M:%S')

                        imap_date = datetime.strptime(mail_date, "%Y-%m-%d %H:%M:%S")
                        is_today = imap_date.date() == date.today()

                        if is_today:
                            mail_date = imap_date.strftime("%H:%M")
                        else:
                            mail_date = imap_date.strftime("%d. %b.")

                        subject = subject.decode(subject_encoding or 'utf-8') if subject_encoding else subject
                        sender = sender.decode(sender_encoding or 'utf-8') if sender_encoding else sender

                        sender_name = extract_name_from_email(sender).rstrip().strip('"')
                        receiver_name = extract_name_from_email(receiver).rstrip().strip('"')

                        email_info = {
                            'id': i,
                            'subject': subject,
                            'sender': sender,
                            'sender_name': sender_name,
                            'receiver': receiver,
                            'receiver_name': receiver_name,
                            'date': mail_date
                        }

                        emails.append(email_info)

                return emails

            else:
                raise ImapFetchException(
                    f"Error while fetching mails from mail box '{folder.value}': Returned status is not OK ({status})"
                )

        except Exception as err:
            raise ImapMailBoxSelectException(f"Error while selecting mail box '{folder.value}': {err}")

    def get_mailboxes(self):
        try:
            status, mailbox_list = self.connection.list()

            if status == "OK":
                mail_boxes = []

                for mailbox in mailbox_list:
                    mail_boxes.append(mailbox)

                return mail_boxes

            else:
                raise ImapFetchMailBoxException(
                    f"Error while fetching mail boxes: Returned status is not OK ({status})"
                )

        except Exception as err:
            raise ImapStatusException(f"Exception while fetching status: {err}")
