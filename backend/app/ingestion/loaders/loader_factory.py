from ..scanner.file_detector import FileType
from .docling_loader import DoclingLoader

class LoaderFactory:
    def __init__(self):
        self.docling_loader=DoclingLoader()

    def get_loader(self,file_type:FileType):

        if file_type in {
             FileType.PDF,
             FileType.MARKDOWN,
             FileType.HTML,
             FileType.DOCX,
             FileType.PPTX

        }:
            return self.docling_loader

        raise ValueError(f"No loader available for this file type:{file_type}")




if __name__ == "__main__":
    factory = LoaderFactory()

    loader = factory.get_loader(FileType.PYTHON)

    print(type(loader).__name__)