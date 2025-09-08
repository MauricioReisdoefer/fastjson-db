class FastJsonError(Exception):
    """Errors related to FastJson-DB implementation"""
    base_message = "FastJson-DB Error"
    
    def __init__(self, message: str):
        # Loads message
        if message is not None:
            self.message = message
        else:
            self.message = "No additional info"
        super().__init__(self.message)

    def __str__(self):
        # Returns when printed
        return f"{self.base_message}: {self.message}"