
from pathlib import Path

from .file_detector import FileType, FileDetector
from .file_filter import FileFilter


class DatasetScanner:

    def __init__(self, root_path: str):
        self.root_path = Path(root_path)
        self.file_detector = FileDetector()
        self.file_filter = FileFilter()

    def scan(self) -> list[Path]:
        files = []

        for path in self.root_path.rglob("*"):
            if not path.is_file():
                continue

            if not self.file_filter.should_include(path):
                continue

            file_type = self.file_detector.detect(path)

            if file_type == FileType.UNKNOWN:
                continue

            files.append(path)

        return files


if __name__ == "__main__":
    scanner = DatasetScanner("../dataset")
    files = scanner.scan()

    print("Total supported files:", len(files))

    for path in files[:20]:
        print(path)
