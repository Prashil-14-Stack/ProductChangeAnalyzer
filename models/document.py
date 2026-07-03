from dataclasses import dataclass, field
from typing import List, Dict, Any

from models.document_page import DocumentPage
from models.business_parameter import BusinessParameter


@dataclass
class Document:
    """
    Enterprise Document Model

    Represents an entire document (DOCX, PDF, OCR, etc.)
    inside Product Change Analyzer.
    """

    # ==========================================================
    # Identity
    # ==========================================================

    filename: str

    file_type: str

    version: int

    # ==========================================================
    # Document Structure
    # ==========================================================

    pages: List[DocumentPage] = field(default_factory=list)

    # ==========================================================
    # Extracted Business Parameters
    # ==========================================================

    parameters: List[BusinessParameter] = field(default_factory=list)

    # ==========================================================
    # Metadata
    # ==========================================================

    metadata: Dict[str, Any] = field(default_factory=dict)

    # ==========================================================
    # Convenience Properties
    # ==========================================================

    @property
    def page_count(self) -> int:
        return len(self.pages)

    @property
    def parameter_count(self) -> int:
        return len(self.parameters)

    @property
    def block_count(self) -> int:
        return sum(page.block_count for page in self.pages)

    @property
    def table_count(self) -> int:
        return sum(page.table_count for page in self.pages)

    # ==========================================================
    # Utility Methods
    # ==========================================================

    def add_page(self, page: DocumentPage):
        self.pages.append(page)

    def add_parameter(self, parameter: BusinessParameter):
        self.parameters.append(parameter)

    def get_parameter(self, name: str):

        for parameter in self.parameters:

            if parameter.normalized_name == name.lower().strip():

                return parameter

        return None

    def summary(self):

        return {

            "filename": self.filename,

            "file_type": self.file_type,

            "version": self.version,

            "page_count": self.page_count,

            "parameter_count": self.parameter_count,

            "block_count": self.block_count,

            "table_count": self.table_count

        }