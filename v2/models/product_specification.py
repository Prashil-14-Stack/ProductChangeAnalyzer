"""
==========================================================
Product Specification Model

Purpose
-------
Represents a complete insurance product specification.

This is the central business object used throughout
ProductChangeAnalyzer V2.

A ProductSpecification contains:

    • Product Information
    • Business Parameters
    • Document Metadata

The comparison engine compares two
ProductSpecification objects.

==========================================================
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List

from models.business_parameter import BusinessParameter


@dataclass
class ProductSpecification:

    # ======================================================
    # Product Information
    # ======================================================

    product_name: str = ""

    product_version: str = ""

    insurer: str = ""

    product_type: str = ""

    document_type: str = ""

    # ======================================================
    # Source Information
    # ======================================================

    source_file: str = ""

    source_format: str = ""

    total_pages: int = 0

    # ======================================================
    # Extracted Business Parameters
    # ======================================================

    parameters: List[BusinessParameter] = field(
        default_factory=list
    )

    # ======================================================
    # Metadata
    # ======================================================

    extraction_timestamp: datetime = field(
        default_factory=datetime.now
    )

    extraction_model: str = ""

    confidence: float = 1.0

    metadata: dict = field(
        default_factory=dict
    )

    # ======================================================
    # Parameter Operations
    # ======================================================

    def add_parameter(
        self,
        parameter: BusinessParameter
    ):

        self.parameters.append(parameter)

    # ------------------------------------------------------

    def get_parameter(
        self,
        parameter_name: str
    ):

        for parameter in self.parameters:

            if parameter.name.lower() == parameter_name.lower():

                return parameter

        return None

    # ------------------------------------------------------

    def has_parameter(
        self,
        parameter_name: str
    ):

        return self.get_parameter(parameter_name) is not None

    # ------------------------------------------------------

    def parameter_count(self):

        return len(self.parameters)

    # ------------------------------------------------------

    def parameters_by_category(
        self,
        category: str
    ):

        return [

            parameter

            for parameter in self.parameters

            if parameter.category.lower() == category.lower()

        ]

    # ------------------------------------------------------

    def categories(self):

        return sorted({

            parameter.category

            for parameter in self.parameters

            if parameter.category

        })

    # ------------------------------------------------------

    def to_dict(self):

        return {

            "product_name": self.product_name,

            "product_version": self.product_version,

            "insurer": self.insurer,

            "product_type": self.product_type,

            "document_type": self.document_type,

            "source_file": self.source_file,

            "source_format": self.source_format,

            "total_pages": self.total_pages,

            "confidence": self.confidence,

            "extraction_model": self.extraction_model,

            "parameters": [

                parameter.to_dict()

                for parameter in self.parameters

            ],

            "metadata": self.metadata

        }

    # ------------------------------------------------------

    def summary(self):

        return {

            "Product": self.product_name,

            "Version": self.product_version,

            "Parameters": self.parameter_count(),

            "Categories": len(self.categories())

        }

    # ------------------------------------------------------

    def __str__(self):

        return (

            f"{self.product_name} "

            f"(Version: {self.product_version})"

        )