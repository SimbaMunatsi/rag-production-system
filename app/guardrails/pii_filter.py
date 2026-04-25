import re

class PIIFilter:
    # Improved regex for standard emails and international phone numbers
    EMAIL_REGEX = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    PHONE_REGEX = r"(\+\d{1,3}\s?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}"

    def contains_pii(self, text: str) -> bool:
        if re.search(self.EMAIL_REGEX, text):
            return True
        if re.search(self.PHONE_REGEX, text):
            return True
        return False