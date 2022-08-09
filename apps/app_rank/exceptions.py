class SessionIDDoesNotExist(Exception):
    def __init__(self, session_id):
        self.session_id = session_id
        self.message = "Invalid Session ID"
        super().__init__(self.message)

    def __str__(self):
        return f'{self.session_id} -> {self.message}'
