from app.ingestion.normalization.document import Document
from app.ingestion.chunking.factory.markdown_chunker import MarkdownChunker

document = Document(
    content="""# PhoenixRAG

PhoenixRAG is a self-healing RAG system.

## Ingestion Pipeline

The ingestion pipeline loads and processes documents.

## Retrieval Pipeline

The retrieval pipeline searches for relevant chunks.
""",
    metadata={
        "source": "test.md",
        "file_type": "markdown"
    }
)

chunker = MarkdownChunker()
chunks = chunker.chunk(document)

for chunk in chunks:
    print("\nChunk ID:", chunk.metadata["chunk_id"])
    print("Metadata:", chunk.metadata)
    print("Content:", chunk.content)