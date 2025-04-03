class HealthException(Exception):
    def __init__(self, message: str, extractor_status: str):
        self.message = message
        self.extractor_status = extractor_status

class ParsingException(Exception):
    def __init__(self, status: int, message: str):
        self.status = status
        self.message = message