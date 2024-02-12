class ImapFetchException(Exception):
    def __init__(self, message="Connection error"):
        self.message = message
        super().__init__(self.message)