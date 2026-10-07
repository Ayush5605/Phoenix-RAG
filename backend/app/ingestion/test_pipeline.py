from pathlib import Path

from app.ingestion.scanner.file_detector import FileDetector
from app.ingestion.loaders.loader_factory import LoaderFactory
from app.ingestion.normalization.normalizer import Normalizer


def main():

    # 1. Select an actual dataset file
    file_path = Path("app/ingestion/scanner/file_detector.py")

    # 2. Detect file type
    detector = FileDetector()
    file_type = detector.detect(file_path)

    print("File type:", file_type)

    # 3. Get appropriate loader
    factory = LoaderFactory()
    loader = factory.get_loader(file_type)

    print("Loader:", type(loader).__name__)

    # 4. Load content
    content = loader.load(file_path)

    print("Loaded content type:", type(content).__name__)

    # 5. Normalize
    normalizer = Normalizer()
    document = normalizer.normalize(content, file_path)

    # 6. Display result
    print("\nDocument content:")
    print(document.content[:500])

    print("\nMetadata:")
    print(document.metadata)


if __name__ == "__main__":
    main()