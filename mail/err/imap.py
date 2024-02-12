class ImapFetchException(Exception):
    def __init__(self, message="Exception while fetching emails"):
        self.message = message
        super().__init__(self.message)


class ImapMailBoxSelectException(Exception):
    def __init__(self, message="Exception while selecting mail box"):
        self.message = message
        super().__init__(self.message)


class ImapFetchMailBoxException(Exception):
    def __init__(self, message="Exception while fetching mail boxes"):
        self.message = message
        super().__init__(self.message)


class ImapStatusException(Exception):
    def __init__(self, message="Exception while fetching status"):
        self.message = message
        super().__init__(self.message)

