from docling.document_converter import DocumentConverter
from .base import DocumentLoader

class DoclingLoader(DocumentLoader):

    def __init__(self):
        self.converter=DocumentConverter()

    def load(self,file_path:str):
        result=self.converter.convert(file_path)

        return result.document