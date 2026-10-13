
from ..base import BaseChunker
from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter
)
from ..chunk_models import Chunk
from langchain_core.documents import Document as LangChainDocument


class MarkdownChunker(BaseChunker):

    def __init__(self):
        self.headers_to_split_on = [
            ("#", "h1"),
            ("##", "h2"),
            ("###", "h3")
        ]

        self.header_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=self.headers_to_split_on,
            strip_headers=False
        )

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=100,
            separators=["\n\n", "\n", ". ", " ", ""]
        )

    def chunk(self, document) -> list[Chunk]:
        markdown_sections = self.header_splitter.split_text(
            document.content
        )

        # Fallback for documents without recognized headings
        if not markdown_sections:
            markdown_sections = [
                LangChainDocument(
                    page_content=document.content,
                    metadata={}
                )
            ]

        chunks = []
        chunk_id = 0

        for section in markdown_sections:
            section_text = section.page_content

            smaller_chunks = self.text_splitter.split_text(
                section_text
            )

            for text in smaller_chunks:
                metadata = {
                    **document.metadata,
                    **section.metadata,
                    "chunk_id": chunk_id
                }

                chunks.append(
                    Chunk(
                        content=text,
                        metadata=metadata
                    )
                )

                chunk_id += 1

        return chunks
