from app.ingestion.loader import DocumentLoader


DATA_DIR = "../dataset"


def main():

    loader = DocumentLoader(DATA_DIR)

    documents = loader.load_documents()

    print("\n================================")
    print("PHOENIXRAG DOCUMENT LOADER TEST")
    print("================================")

    print(f"\nTotal documents loaded: {len(documents)}")

    if documents:

        print("\nFirst document:")
        print("----------------")

        print(documents[0].page_content[:1000])

        print("\nMetadata:")
        print("---------")

        print(documents[0].metadata)


if __name__ == "__main__":
    main()