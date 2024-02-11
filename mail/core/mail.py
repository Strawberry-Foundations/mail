from mail.imap.client import ImapServer
from mail.core.config import config

imap = ImapServer(config.imap_host, config.imap_port)
