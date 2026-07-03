from dataclasses import dataclass, field
from typing import List, Dict, Any

from models.document_block import DocumentBlock
from models.document_table import DocumentTable


@dataclass
class DocumentPage:
    """
    Represents one page of a document.
    """

    # ==========================================
    # Identity
    # ==========================================

    page_number: int

    # ==========================================
    # Layout Information
    # ==========================================

    width: float = 0

    height: float = 0

    rotation: int = 0

    # ==========================================
    # Content
    # ==========================================

    blocks: List[DocumentBlock] = field(default_factory=list)

    tables: List[DocumentTable] = field(default_factory=list)

    # ==========================================
    # Metadata
    # ==========================================

    metadata: Dict[str, Any] = field(default_factory=dict)

    # ==========================================
    # Convenience Properties
    # ==========================================

    @property
    def block_count(self):

        return len(self.blocks)

    @property
    def table_count(self):

        return len(self.tables)

    # ==========================================
    # Utility Methods
    # ==========================================

    def add_block(self, block: DocumentBlock):

        self.blocks.append(block)

    def add_table(self, table: DocumentTable):

        self.tables.append(table)