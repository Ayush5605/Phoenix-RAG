from factory.markdown_chunker import MarkdownChunker
from factory.code_chunker import CodeChunker
from factory.pdf_chunker import PdfChunker
from factory.json_chunker import JsonChunker
from factory.yaml_chunker import YamlChunker
from factory.text_chunker import TextChunker


class ChunkerFactory:

    def __init__(self):
        self.chunkers={
            "markdown":MarkdownChunker(),
            "pyhton":CodeChunker(),
            "javscript":CodeChunker(),
            "typescript":CodeChunker(),
            "pdf":PdfChunker(),
            "yaml":YamlChunker(),
            "json":JsonChunker(),
            "text":TextChunker()
        }


    def get_chunker(self,document):
        file_type=document.metadata['file_type']

        if file_type not in self.chunkers:
            raise ValueError(f"No chunker available for file type :{file_type}")

        return self.chunkers[file_type]
