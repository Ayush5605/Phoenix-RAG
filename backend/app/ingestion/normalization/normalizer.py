from pathlib import Path
from .document import Document

class Normalizer:

    def normalize(self,content:str,file_path:str)->Document:
        path=Path(file_path)

        metadata={
            "source":str(path),
            "file_name":path.name,
            "extension":path.suffix.lower()
        }

        return Document(
            content=content,
            metadata=metadata
        )