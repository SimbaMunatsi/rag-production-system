import re

class DocumentCleaner:
    def clean(self, documents):
        cleaned_docs = []
        for doc in documents:
            text = doc.page_content
            if not text:
                continue
            # Remove excessive whitespace and newlines
            text = re.sub(r"\s+", " ", text)
            doc.page_content = text.strip()
            cleaned_docs.append(doc)
        return cleaned_docs