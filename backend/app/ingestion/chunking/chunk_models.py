from dataclasses import dataclass
from typing import Any

@dataclass
class Chunk:
    content:str
    metadata:dict[str,Any]
