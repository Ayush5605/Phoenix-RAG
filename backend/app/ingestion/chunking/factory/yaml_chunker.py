import yaml

from langchain_text_splitters import RecursiveCharacterTextSplitter

from ..base import BaseChunker
from ..chunk_models import Chunk


class YAMLChunker(BaseChunker):

    def __init__(self):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100,
            separators=["\n\n", "\n", " ", ""]
        )

    def chunk(self, document) -> list[Chunk]:
        try:
            data = yaml.safe_load(document.content)
        except yaml.YAMLError:
            text_chunks = self.splitter.split_text(document.content)
        else:
            if isinstance(data, list):
                items = data
            elif isinstance(data, dict):
                items = [
                    {key: value}
                    for key, value in data.items()
                ]
            elif data is None:
                items = []
            else:
                items = [data]

            text_chunks = []
            current_items = []

            for item in items:
                serialized = yaml.safe_dump(
                    item,
                    sort_keys=False,
                    allow_unicode=True
                ).strip()

                candidate = "\n".join(current_items + [serialized])

                if current_items and len(candidate) > 1000:
                    text_chunks.append("\n".join(current_items))
                    current_items = [serialized]
                else:
                    current_items.append(serialized)

            if current_items:
                text_chunks.append("\n".join(current_items))

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
