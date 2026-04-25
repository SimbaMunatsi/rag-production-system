from langchain_text_splitters import RecursiveCharacterTextSplitter

class DocumentChunker:
    def __init__(self):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=600,
            chunk_overlap=120,
            separators=[
                "\n\n",
                "\n",
                ". ",
                " "
            ]
        )

    def chunk(self, documents):
        chunks = self.splitter.split_documents(documents)
        return chunks