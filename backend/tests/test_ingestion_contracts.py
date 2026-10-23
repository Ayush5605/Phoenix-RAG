import sys
import types
import unittest
from unittest.mock import patch

from app.ingestion.chunking.base import BaseChunker
from app.ingestion.loaders.base import DocumentLoader
from app.ingestion.loaders.loader_factory import LoaderFactory
from app.ingestion.scanner.file_detector import FileType


class LoaderFactoryTests(unittest.TestCase):
    def test_text_types_share_text_loader(self):
        factory = LoaderFactory()

        for file_type in LoaderFactory.TEXT_FILE_TYPES:
            with self.subTest(file_type=file_type):
                self.assertIs(factory.get_loader(file_type), factory.text_loader)

    def test_docling_loader_is_created_lazily_and_reused(self):
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

            first_loader = factory.get_loader(FileType.PDF)
            second_loader = factory.get_loader(FileType.HTML)

        self.assertIs(first_loader, second_loader)
        self.assertIsInstance(first_loader, FakeDoclingLoader)

    def test_unsupported_types_raise_clear_error(self):
        factory = LoaderFactory()

        for file_type in (FileType.IMAGE, FileType.XLSX, FileType.UNKNOWN):
            with self.subTest(file_type=file_type):
                with self.assertRaisesRegex(
                    ValueError, f"No loader available for file type: {file_type}"
                ):
                    factory.get_loader(file_type)


class AbstractContractTests(unittest.TestCase):
    def test_loader_base_cannot_be_instantiated_without_load(self):
        with self.assertRaises(TypeError):
            DocumentLoader()

    def test_chunker_base_cannot_be_instantiated_without_chunk(self):
        with self.assertRaises(TypeError):
            BaseChunker()


if __name__ == "__main__":
    unittest.main()
