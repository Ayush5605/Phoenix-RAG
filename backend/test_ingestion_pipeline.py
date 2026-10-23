import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import patch

from app.ingestion.chunking.chunker_factory import ChunkerFactory
from app.ingestion.chunking.factory.text_chunker import TextChunker
from app.ingestion.loaders.base import DocumentLoader
from app.ingestion.loaders.loader_factory import LoaderFactory
from app.ingestion.normalization.document import Document
from app.ingestion.pipeline import IngestionPipeline
from app.ingestion.scanner.dataset_scanner import DatasetScanner
from app.ingestion.scanner.file_detector import (
    FileType,
    INGESTIBLE_FILE_TYPES,
)


class LoaderFactoryTests(unittest.TestCase):
    def test_text_file_types_use_the_text_loader(self):
        factory = LoaderFactory()

        for file_type in (
            FileType.MARKDOWN,
            FileType.TEXT,
            FileType.PYTHON,
            FileType.JAVASCRIPT,
            FileType.TYPESCRIPT,
            FileType.JSON,
            FileType.YAML,
            FileType.SVG,
        ):
            with self.subTest(file_type=file_type):
                self.assertIs(factory.get_loader(file_type), factory.text_loader)

    def test_docling_loader_is_lazy_and_shared(self):
        class FakeDoclingLoader(DocumentLoader):
            def load(self, file_path: str):
                return file_path

        fake_module = types.ModuleType(
            "app.ingestion.loaders.docling_loader"
        )
        fake_module.DoclingLoader = FakeDoclingLoader

        with patch.dict(
            sys.modules,
            {"app.ingestion.loaders.docling_loader": fake_module},
        ):
            factory = LoaderFactory()
            self.assertIsNone(factory._docling_loader)

            pdf_loader = factory.get_loader(FileType.PDF)
            docx_loader = factory.get_loader(FileType.DOCX)
            pptx_loader = factory.get_loader(FileType.PPTX)
            html_loader = factory.get_loader(FileType.HTML)

        self.assertIs(pdf_loader, docx_loader)
        self.assertIs(pdf_loader, pptx_loader)
        self.assertIs(pdf_loader, html_loader)

    def test_unimplemented_types_raise_clear_errors(self):
        factory = LoaderFactory()

        for file_type in (FileType.IMAGE, FileType.XLSX, FileType.UNKNOWN):
            with self.subTest(file_type=file_type):
                with self.assertRaisesRegex(
                    ValueError,
                    f"No loader available for file type: {file_type}",
                ):
                    factory.get_loader(file_type)


class ChunkerFactoryTests(unittest.TestCase):
    def test_every_ingestible_file_type_has_a_chunker(self):
        factory = ChunkerFactory()

        for file_type in INGESTIBLE_FILE_TYPES:
            document = Document(
                content="Example content",
                metadata={"file_type": file_type.value},
            )
            with self.subTest(file_type=file_type):
                self.assertIsNotNone(factory.get_chunker(document))

    def test_docx_and_pptx_use_text_chunker(self):
        factory = ChunkerFactory()

        for file_type in (FileType.DOCX, FileType.PPTX):
            document = Document(
                content="Extracted document content",
                metadata={"file_type": file_type.value},
            )
            with self.subTest(file_type=file_type):
                self.assertIsInstance(factory.get_chunker(document), TextChunker)

    def test_unimplemented_types_raise_clear_errors(self):
        factory = ChunkerFactory()

        for file_type in (FileType.IMAGE, FileType.XLSX, FileType.UNKNOWN):
            document = Document(
                content="",
                metadata={"file_type": file_type.value},
            )
            with self.subTest(file_type=file_type):
                with self.assertRaisesRegex(
                    ValueError,
                    f"No chunker available for file type: {file_type.value}",
                ):
                    factory.get_chunker(document)


class DatasetScannerTests(unittest.TestCase):
    def test_scan_returns_only_ingestible_file_types(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            expected = {"readme.md", "manual.docx", "slides.pptx"}
            file_names = expected | {
                "workbook.xlsx",
                "photo.png",
                "unknown.bin",
            }
            for name in file_names:
                (root / name).write_text("content", encoding="utf-8")

            scanned_names = {
                path.name for path in DatasetScanner(root).scan()
            }

        self.assertEqual(scanned_names, expected)


class IngestionPipelineTests(unittest.TestCase):
    def test_process_markdown_file_returns_metadata_enriched_chunks(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "guide.md"
            path.write_text(
                "# Guide\n\nPipeline content.",
                encoding="utf-8",
            )

            chunks = IngestionPipeline().process_file(str(path))

        self.assertTrue(chunks)
        self.assertTrue(
            all(chunk.metadata["file_type"] == "markdown" for chunk in chunks)
        )
        self.assertTrue(
            all(chunk.metadata["file_name"] == "guide.md" for chunk in chunks)
        )
        self.assertEqual(
            [chunk.metadata["chunk_id"] for chunk in chunks],
            list(range(len(chunks))),
        )


if __name__ == "__main__":
    unittest.main()
