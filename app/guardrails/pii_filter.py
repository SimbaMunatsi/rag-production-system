import re


class PIIFilter:

    EMAIL_REGEX = r"\S+@\S+"
    PHONE_REGEX = r"\+?\d{10,13}"

    def contains_pii(self, text: str) -> bool:

        if re.search(self.EMAIL_REGEX, text):
            return True

        if re.search(self.PHONE_REGEX, text):
            return True

        return False