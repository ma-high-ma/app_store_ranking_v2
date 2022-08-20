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


class NoPreviousAppDataPresent(Exception):
    def __init__(self, app_handle):
        self.app_handle = app_handle
        self.message = "App Ranks were never scraped for this keyword before this instance"
        super().__init__(self.message)

    def __str__(self):
        return f'{self.app_handle} -> {self.message}'


class PageNotScrapedSuccessfully(Exception):
    def __init__(self, **kwargs):
        self.app_handle = kwargs.get('app_handle', '')
        self.page_no = kwargs.get('page_no', '')
        self.message = "Page was not scraped successfully"
        super().__init__(self.message)


class AppPageScrapingMaxRetriesReached(Exception):
    pass


class NoCompletedRankDeltaProcessorFound(Exception):
    def __init__(self):
        self.message = "No Rank Delta Processor session found with status = completed"
        super().__init__(self.message)


class TaskInterruptedDueToAnException(Exception):
    pass
