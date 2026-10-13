from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    Language
)

from ..base import BaseChunker
from ..chunk_models import Chunk


class CodeChunker(BaseChunker):

    def __init__(self, language: Language = Language.PYTHON):
        self.splitter = RecursiveCharacterTextSplitter.from_language(
            language=language,
            chunk_size=1000,
            chunk_overlap=150
        )

    def chunk(self, document) -> list[Chunk]:
        code_chunks = self.splitter.split_text(document.content)

        chunks = []

        for chunk_id, text in enumerate(code_chunks):
            metadata = {
                **document.metadata,
                "chunk_id": chunk_id
            }

            chunks.append(
                Chunk(
                    content=text,
                    metadata=metadata
                )
            )

        return chunks