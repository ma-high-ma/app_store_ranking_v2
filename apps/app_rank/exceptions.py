class SessionIDDoesNotExist(Exception):
    def __init__(self, session_id):
        self.session_id = session_id
        self.message = "Invalid Session ID"
        super().__init__(self.message)

    def __str__(self):
        return f'{self.session_id} -> {self.message}'


class NoPreviousAppRankForGivenKeyword(Exception):
    def __init__(self, keyword):
        self.keyword = keyword
        self.message = "App Ranks were never scraped for this keyword before this instance"
        super().__init__(self.message)

    def __str__(self):
        return f'{self.keyword} -> {self.message}'
