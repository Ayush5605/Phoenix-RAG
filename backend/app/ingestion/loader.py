from pathlib import Path

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader
)


class DocumentLoader:

    def __init__(self, data_dir: str):
        self.data_dir = Path(data_dir)

    def load_documents(self):

        documents = []

        if not self.data_dir.exists():
            raise FileNotFoundError(
                f"Data directory not found: {self.data_dir}"
            )

        files = [
            file_path
            for file_path in self.data_dir.rglob("*")
            if file_path.is_file()
            and file_path.suffix.lower() in [".pdf", ".txt", ".md"]
        ]

        print(f"Found {len(files)} files")

        for index, file_path in enumerate(files, start=1):

            print(
                f"[{index}/{len(files)}] Loading: {file_path.name}"
            )

            try:

                extension = file_path.suffix.lower()

                if extension == ".pdf":

                    loader = PyPDFLoader(str(file_path))
                    loaded_docs = loader.load()

                else:

                    loader = TextLoader(
                        str(file_path),
                        encoding="utf-8"
                    )
                    loaded_docs = loader.load()

                documents.extend(loaded_docs)

            except Exception as e:

                print(
                    f"⚠️ Failed to load {file_path}: {e}"
                )

        print(
            f"\nSuccessfully loaded {len(documents)} documents"
        )

        return documents