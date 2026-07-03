from dataclasses import dataclass
from typing import List

from models.document import Document
from models.business_parameter import BusinessParameter


@dataclass
class SemanticIndex:
    """
    Enterprise Semantic Index

    Represents one searchable semantic record
    inside the Semantic Repository.

    Each BusinessParameter is converted into
    one SemanticIndex object.
    """

    # ==========================================================
    # Source
    # ==========================================================

    document: Document

    parameter: BusinessParameter

    # ==========================================================
    # Embedding
    # ==========================================================

    embedding: List[float]

    # ==========================================================
    # Convenience Properties
    # ==========================================================

    @property
    def version(self):

        return self.document.version

    @property
    def filename(self):

        return self.document.filename

    @property
    def parameter_name(self):

        return self.parameter.name

    @property
    def parameter_value(self):

        return self.parameter.value

    @property
    def page_number(self):

        return self.parameter.page_number

    @property
    def category(self):

        return self.parameter.category

    @property
    def confidence(self):

        return self.parameter.confidence

    # ==========================================================
    # Utility
    # ==========================================================

    def summary(self):

        return {

            "document": self.filename,

            "version": self.version,

            "parameter": self.parameter_name,

            "category": self.category,

            "page": self.page_number,

            "confidence": self.confidence

        }