from ..scanner.file_detector import FileType
from .base import DocumentLoader
from .text_loader import TextLoader


class LoaderFactory:
    TEXT_FILE_TYPES = frozenset({
        FileType.MARKDOWN,
        FileType.TEXT,
        FileType.PYTHON,
        FileType.JAVASCRIPT,
        FileType.TYPESCRIPT,
        FileType.JSON,
        FileType.YAML,
        FileType.SVG,
    })
    DOCLING_FILE_TYPES = frozenset({
        FileType.PDF,
        FileType.DOCX,
        FileType.PPTX,
        FileType.HTML,
    })

    def __init__(self):
        self.text_loader = TextLoader()
        self._docling_loader: DocumentLoader | None = None

    def get_loader(self, file_type: FileType) -> DocumentLoader:
        if file_type in self.TEXT_FILE_TYPES:
            return self.text_loader

        if file_type in self.DOCLING_FILE_TYPES:
            if self._docling_loader is None:
                from .docling_loader import DoclingLoader

                self._docling_loader = DoclingLoader()
            return self._docling_loader

        raise ValueError(f"No loader available for file type: {file_type}")


if __name__ == "__main__":
    from pathlib import Path

    from ..scanner.file_detector import FileDetector

    file_path = Path("app/ingestion/scanner/file_detector.py")
    file_type = FileDetector().detect(file_path)
    loader = LoaderFactory().get_loader(file_type)

    print("File type:", file_type)
    print("Loader:", type(loader).__name__)
    print("\nContent:")
    print(loader.load(str(file_path))[:500])
