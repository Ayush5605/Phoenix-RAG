from ..scanner.file_detector import FileType
from .docling_loader import DoclingLoader
from .text_loader import TextLoader

class LoaderFactory:
    def __init__(self):
        self.docling_loader=DoclingLoader()
        self.text_loader=TextLoader()

    def get_loader(self,file_type:FileType):

        if file_type in {
             FileType.PDF,
             FileType.MARKDOWN,
             FileType.HTML,
             FileType.DOCX,
             FileType.PPTX

        }:
            return self.docling_loader

        if file_type in{
             FileType.TEXT,
            FileType.PYTHON,
            FileType.JAVASCRIPT,
            FileType.TYPESCRIPT,
            FileType.JSON,
            FileType.YAML,
            FileType.SVG

        }:
            return self.text_loader

        raise ValueError(f"No loader available for this file type:{file_type}")




if __name__ == "__main__":
    from pathlib import Path
    from ..scanner.file_detector import FileDetector

    file_path = Path("app/ingestion/scanner/file_detector.py")

    detector = FileDetector()
    file_type = detector.detect(file_path)

    print("File type:", file_type)

    factory = LoaderFactory()
    loader = factory.get_loader(file_type)

    print("Loader:", type(loader).__name__)

    content = loader.load(file_path)

    print("\nContent:")
    print(content[:500])