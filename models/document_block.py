from dataclasses import dataclass
from typing import Tuple


@dataclass
class DocumentBlock:
    """
    Represents a block of text extracted from a document.
    """

    page: int

    block_number: int

    block_type: int

    text: str

    bbox: Tuple[float, float, float, float]