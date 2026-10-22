
from app.ingestion.normalization.document import Document
from app.ingestion.chunking.chunker_factory import ChunkerFactory


def main():
    factory = ChunkerFactory()

    test_documents = [
        Document(
            content="# PhoenixRAG\n\nA self-healing RAG system.",
            metadata={"source": "test.md", "file_type": "markdown"}
        ),
        Document(
            content="def hello():\n    print('Hello PhoenixRAG')",
            metadata={"source": "test.py", "file_type": "python"}
        ),
        Document(
            content='{"name": "PhoenixRAG", "version": 1}',
            metadata={"source": "test.json", "file_type": "json"}
        ),
        Document(
            content="PhoenixRAG processes documents.\nIt retrieves relevant chunks.",
            metadata={"source": "test.txt", "file_type": "text"}
        ),
    ]

    for document in test_documents:
        print(f"\n{'=' * 50}")
        print("File type:", document.metadata["file_type"])

        try:
            chunker = factory.get_chunker(document)
            chunks = chunker.chunk(document)

            print("Chunker:", type(chunker).__name__)
            print("Total chunks:", len(chunks))

            for chunk in chunks:
                print("Metadata:", chunk.metadata)
                print("Content:", chunk.content)

        except Exception as error:
            print("Error:", error)


if __name__ == "__main__":
    main()
