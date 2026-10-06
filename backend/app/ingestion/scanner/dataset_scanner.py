from pathlib import Path

from .file_detector import FileType,FileDetector
from .file_filter import FileFilter


class DatasetScanner:
    def __init__(self,root_path:str):
        self.root_path=Path(root_path)
        self.file_detector=FileDetector()
        self.file_filter=FileFilter()

    def scan(self):
        

        for path in self.root_path.rglob("*"):
            if path.is_file():

                if not self.file_filter.should_include(path):
                    continue
                
                file_type=self.file_detector.detect(path)

                print(path,file_type)



if __name__ == "__main__":
    scanner = DatasetScanner("../dataset")
    scanner.scan()