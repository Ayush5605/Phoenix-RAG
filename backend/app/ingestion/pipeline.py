
from pathlib import Path

from .scanner.file_detector import FileDetector
from .scanner.dataset_scanner import DatasetScanner
from .loaders.loader_factory import LoaderFactory
from .normalization.normalizer import Normalizer
from .chunking.chunker_factory import ChunkerFactory


class IngestionPipeline:
    def __init__(self):
        self.file_detector = FileDetector()
        self.loader_factory = LoaderFactory()
        self.normalizer = Normalizer()
        self.chunker_factory = ChunkerFactory()

    def process_file(self, file_path: str):
        path = Path(file_path)

        if not path.is_file():
            raise FileNotFoundError(f"File not found: {path}")

        # 1. Detect file type
        file_type = self.file_detector.detect(path)

        # 2. Load raw content
        loader = self.loader_factory.get_loader(file_type)
        raw_content = loader.load(str(path))

        # 3. Normalize content and extract metadata
        document = self.normalizer.normalize(
            raw_content,
            str(path)
        )

        # 4. Select the appropriate chunker
        chunker = self.chunker_factory.get_chunker(document)

        # 5. Generate chunks
        chunks = chunker.chunk(document)

        return chunks

    def process_dataset(self, root_path: str):
        scanner = DatasetScanner(root_path)
        file_paths = scanner.scan()

        all_chunks = []
        failed_files = []

        print(f"Discovered {len(file_paths)} files.")

        for index, file_path in enumerate(file_paths, start=1):
            try:
                chunks = self.process_file(str(file_path))
                all_chunks.extend(chunks)

                print(
                    f"[{index}/{len(file_paths)}] "
                    f"{file_path.name}: {len(chunks)} chunks"
                )

            except Exception as error:
                failed_files.append((str(file_path), str(error)))
                print(f"Failed: {file_path} — {error}")

        print("\n--- Ingestion Summary ---")
        print(f"Files discovered: {len(file_paths)}")
        print(f"Chunks generated: {len(all_chunks)}")
        print(f"Failed files: {len(failed_files)}")

        if failed_files:
            print("\n--- Failed Files ---")
            for file_path, error in failed_files:
                print(f"{file_path}: {error}")

        return all_chunks


if __name__ == "__main__":
    pipeline = IngestionPipeline()

    chunks = pipeline.process_dataset(
        "../dataset/data/security/CheatSheetSeries"
    )

    print(f"\nTotal chunks returned: {len(chunks)}")
