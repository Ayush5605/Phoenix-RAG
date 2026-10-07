from pathlib import Path
from .document import Document
from .cleaner import Cleaner

class Normalizer:

    def __init__(self):
        self.cleaner=Cleaner()

    def normalize(self,content:str,file_path:str)->Document:
        cleaned_content=self.cleaner.clean(content)
        path=Path(file_path)

        metadata={
            "source":str(path),
            "file_name":path.name,
            "extension":path.suffix.lower()
        }

        return Document(
            content=cleaned_content,
            metadata=metadata
        )


if __name__ == "__main__":

    normalizer = Normalizer()

    content = "Hello   \n\n\n\nPhoenixRAG   \n\nThis is a test.   "

    document = normalizer.normalize(
        content,
        "example.py"
    )

    print("CONTENT:")
    print(repr(document.content))

    print("\nMETADATA:")
    print(document.metadata)