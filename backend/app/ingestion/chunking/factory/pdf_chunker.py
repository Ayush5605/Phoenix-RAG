from ..base import BaseChunker
from langchain_text_splitters import RecursiveCharacterTextSplitter
from ..chunk_models import Chunk

class PdfChunker(BaseChunker):

    def __init__(self):
        self.splitter=RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=150,
            separators=["\n\n", "\n", ". ", " ", ""]
        )

    def chunk(self,document)->list[Chunk]:
        text_chunks=self.splitter.split_text(document.content)

        chunks=[]

        for chunk_id,text in enumerate(text_chunks):
            metadata={
                **document.metadata,
                "chunk_id":chunk_id
            }

            chunks.append(
                Chunk(content=text,
                      metadata=metadata
                      )
                )

        return chunks