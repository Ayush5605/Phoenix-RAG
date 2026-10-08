from pathlib import Path
from ..scanner.file_detector import FileDetector


class MetaDataExtractor:

    def __init__(self):
        self.file_detector=FileDetector()

    def extract(self,file_path:str):
        path=Path(file_path)

        file_type=self.file_detector.detect(path)

        metadata={
            "source":str(path),
            "file_name":path.name,
            "extension":path.suffix.lower(),
            "file_type":file_type.value,
            "directory":path.parent.name
        }

        return metadata



if __name__ =="__main__":
    metadata=MetaDataExtractor()
    print(metadata.extract(r"D:\Projects\PhoenixRAG\dataset\data\Engineer\API\fastapi\README.md"))