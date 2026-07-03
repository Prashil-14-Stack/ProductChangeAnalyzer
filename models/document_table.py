from dataclasses import dataclass, field
from typing import List


@dataclass
class DocumentTable:
    """
    Represents a detected table within a document.
    """

    page: int

    table_number: int

    rows: List[List[str]] = field(default_factory=list)