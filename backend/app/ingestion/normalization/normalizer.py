from pathlib import Path
from .document import Document
from .cleaner import Cleaner
from ..metadata.metadata_extractor import MetaDataExtractor


class Normalizer:

    def __init__(self):
        self.cleaner=Cleaner()
        self.metadata_extractor=MetaDataExtractor()

    def normalize(self,content:str,file_path:str)->Document:
        if hasattr(content, "export_to_markdown"):
            content = content.export_to_markdown()
        cleaned_content=self.cleaner.clean(content)
        path=Path(file_path)

        metadata=self.metadata_extractor.extract(path)

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