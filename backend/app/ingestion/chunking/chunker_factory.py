
from ..normalization.document import Document

from .factory.markdown_chunker import MarkdownChunker
from .factory.code_chunker import CodeChunker
from .factory.pdf_chunker import PdfChunker
from .factory.json_chunker import JSONChunker
from .factory.yaml_chunker import YAMLChunker
from .factory.text_chunker import TextChunker

from langchain_text_splitters import Language


class ChunkerFactory:

    def __init__(self):
        self.chunkers = {
            "markdown": MarkdownChunker(),
            "pdf": PdfChunker(),
            "json": JSONChunker(),
            "yaml": YAMLChunker(),
            "text": TextChunker(),
            "html": TextChunker(),
            "svg": TextChunker(),
        }

        self.code_languages = {
            "python": Language.PYTHON,
            "javascript": Language.JS,
            "typescript": Language.TS,
        }

    def get_chunker(self, document: Document):
        file_type = document.metadata.get("file_type")

        if file_type in self.code_languages:
            return CodeChunker(
                language=self.code_languages[file_type]
            )

        chunker = self.chunkers.get(file_type)

        if chunker is None:
            raise ValueError(
                f"No chunker available for file type: {file_type}"
            )

        return chunker