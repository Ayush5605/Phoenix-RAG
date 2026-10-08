from abc import ABC,abstractmethod

from ..normalization.document import Document
from .chunk_models import Chunk

class BaseChunker(ABC):
    def chunk(self,document:Document)->list[Chunk]:
        pass