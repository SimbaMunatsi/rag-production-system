from langchain_community.document_loaders import (
    DirectoryLoader,
    TextLoader,
    PyPDFLoader,
    UnstructuredMarkdownLoader,
    CSVLoader,
    UnstructuredHTMLLoader
)


class DocumentLoader:

    def __init__(self, path: str):
        self.path = path

    def load(self):


        loaders = [
            DirectoryLoader(
                self.path,
                glob="**/*.txt",
                loader_cls=TextLoader,
                silent_errors=True
            ),
            DirectoryLoader(
                self.path,
                glob="**/*.pdf",
                loader_cls=PyPDFLoader,
                silent_errors=True
            ),
            DirectoryLoader(
                self.path,
                glob="**/*.md",
                loader_cls=UnstructuredMarkdownLoader,
                silent_errors=True
            ),
            DirectoryLoader(
                self.path,
                glob="**/*.csv",
                loader_cls=CSVLoader,
                silent_errors=True
            ),
            DirectoryLoader(
                self.path,
                glob="**/*.html",
                loader_cls=UnstructuredHTMLLoader,
                silent_errors=True
            )
        ]

        documents = []

        

        for loader in loaders:
            loaded_docs = loader.load()
            documents.extend(loaded_docs) 

        return documents