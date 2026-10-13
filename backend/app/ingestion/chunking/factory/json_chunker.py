
import json

from langchain_text_splitters import RecursiveCharacterTextSplitter

from ..base import BaseChunker
from ..chunk_models import Chunk


class JSONChunker(BaseChunker):

    def __init__(self):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100,
            separators=["\n", ",", " ", ""]
        )

    def chunk(self, document) -> list[Chunk]:
        try:
            data = json.loads(document.content)
        except json.JSONDecodeError:
            # Fall back to ordinary text splitting for invalid JSON.
            text_chunks = self.splitter.split_text(document.content)
        else:
            # Preserve top-level objects or array elements where possible.
            if isinstance(data, dict):
                items = [data]
            elif isinstance(data, list):
                items = data
            else:
                items = [data]

            text_chunks = []
            current_items = []

            for item in items:
                serialized = json.dumps(item, ensure_ascii=False, indent=2)

                candidate = current_items + [serialized]
                candidate_text = "\n".join(candidate)

                if (
                    current_items
                    and len(candidate_text) > 1000
                ):
                    text_chunks.append("\n".join(current_items))
                    current_items = [serialized]
                else:
                    current_items = candidate

            if current_items:
                text_chunks.append("\n".join(current_items))

            # Split any individual item that exceeds the target size.
            final_chunks = []

            for text in text_chunks:
                if len(text) > 1000:
                    final_chunks.extend(self.splitter.split_text(text))
                else:
                    final_chunks.append(text)

            text_chunks = final_chunks

        chunks = []

        for chunk_id, text in enumerate(text_chunks):
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
