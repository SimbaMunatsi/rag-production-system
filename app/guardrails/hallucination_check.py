class HallucinationChecker:

    def grounded(self, answer: str, context_docs):

        context_text = " ".join([doc.page_content for doc in context_docs])

        if answer.lower() in context_text.lower():
            return True

        return False