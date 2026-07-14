"""
==========================================================
Enterprise Layout Analyzer

Coordinates the document layout understanding pipeline.

==========================================================
"""

from legacy.pdf_engine_v1.core.layout.layout_classifier import LayoutClassifier
from legacy.pdf_engine_v1.core.layout.figure_detector import FigureDetector
from legacy.pdf_engine_v1.core.layout.list_detector import ListDetector
from legacy.pdf_engine_v1.core.layout.reading_order import ReadingOrder
from legacy.pdf_engine_v1.core.layout.relationship_builder import RelationshipBuilder
from legacy.pdf_engine_v1.core.layout.table_structure_builder import TableStructureBuilder
from legacy.pdf_engine_v1.core.layout.section_builder import SectionBuilder
from legacy.pdf_engine_v1.core.layout.logical_line_builder import LogicalLineBuilder
from legacy.pdf_engine_v1.core.layout.layout_feature_extractor import LayoutFeatureExtractor
from legacy.pdf_engine_v1.core.layout.heading_detector import HeadingDetector
from legacy.pdf_engine_v1.core.layout.table_reconstructor import TableReconstructor

class LayoutAnalyzer:

    def __init__(self):

        self.classifier = LayoutClassifier()

        self.reading_order = ReadingOrder()

        self.relationship_builder = RelationshipBuilder()

        self.table_builder = TableStructureBuilder()

        self.figure_detector = FigureDetector()

        self.list_detector = ListDetector()

        self.section_builder = SectionBuilder()

        self.logical_line_builder = LogicalLineBuilder()

        self.feature_extractor = LayoutFeatureExtractor()

        self.heading_detector = HeadingDetector()

        self.table_reconstructor = TableReconstructor()

    # ======================================================
    # Analyze
    # ======================================================

    def analyze(self, document):

        # --------------------------------------------------
        # 1. Classify Layout Blocks
        # --------------------------------------------------

        document = self.classifier.process(document)

        # --------------------------------------------------
        # 2. Build Reading Order
        # --------------------------------------------------

        document = self.reading_order.process(document)

        # --------------------------------------------------
        # 3. Build Spatial Relationships
        # --------------------------------------------------

        document = self.relationship_builder.process(document)

        # --------------------------------------------------
        # 4. Detect Table Structures
        # --------------------------------------------------

        document = self.table_builder.process(document)

        # --------------------------------------------------
        # 5. Detect Figures
        # --------------------------------------------------

        document = self.figure_detector.process(document)

        # --------------------------------------------------
        # 6. Detect Lists
        # --------------------------------------------------

        document = self.list_detector.process(document)

        # --------------------------------------------------
        # 7. Build Sections
        # --------------------------------------------------

        #document = self.section_builder.process(document)

        document = self.table_builder.process(document)

        document = self.feature_extractor.process(document)

        document = self.heading_detector.process(document)

        #document = self.table_reconstructor.process(document)

        return document