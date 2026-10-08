from pathlib import Path
from ..scanner.file_detector import FileDetector


class MetaDataExtractor:

    def __init__(self):
        self.file_detector=FileDetector()

    def extract(self,file_path:str):
        path=Path(file_path)

        file_type=self.file_detector(path)

        metadata={
            "source":str(path),
            "file_name":path.name,
            "extension":path.suffix.lower(),
            "file_type":file_type.value,
            "directory":path.parent.name
        }

        return metadata