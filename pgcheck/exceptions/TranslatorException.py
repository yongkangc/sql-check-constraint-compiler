class EmptyNameException(Exception):
    def __init__(self):
        super().__init__()
        self.message = "Unable to extract value"