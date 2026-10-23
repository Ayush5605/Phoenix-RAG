from abc import ABC, abstractmethod

from ..normalization.document import Document
from .chunk_models import Chunk


class BaseChunker(ABC):
    @abstractmethod
    def chunk(self, document: Document) -> list[Chunk]:
        raise NotImplementedError
