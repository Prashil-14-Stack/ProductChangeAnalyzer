from readers.pdf_reader import PDFReader

from processors.layout_normalizer import LayoutNormalizer
from processors.layout_classifier import LayoutClassifier
from processors.section_detector_pdf import SectionDetectorPDF
from processors.business_parameter_extractor_pdf import BusinessParameterExtractorPDF
from processors.reading_order_engine import ReadingOrderEngine


class PDFMVPExtractor:
    """
    ==========================================================
    Sprint 2 MVP PDF Extraction Pipeline

    Converts

        PDF

    into

        BusinessParameter objects

    using deterministic logic only.

    Pipeline

        PDF
            ↓
        RAWDICT Reader
            ↓
        Layout Normalizer
            ↓
        Layout Classifier
            ↓
        Business Block Detector
            ↓
        Business Parameter Builder

    No OCR
    No Camelot
    No GPT

    ==========================================================
    """

    def __init__(self):

        self.reader = PDFReader()

        self.normalizer = LayoutNormalizer()

        self.classifier = LayoutClassifier()

        self.section_detector = SectionDetectorPDF()

        self.parameter_extractor = BusinessParameterExtractorPDF()

        self.reading_order = ReadingOrderEngine()

    # ==========================================================
    # Extract
    # ==========================================================

    def extract(

        self,

        uploaded_file

    ):

        # ------------------------------------------------------
        # Read PDF
        # ------------------------------------------------------

        document = self.reader.read(

            uploaded_file

        )
        document = self.normalizer.normalize(

            document

        )

        document = self.reading_order.process(

            document

        )
        print("\n")
        print("=" * 100)
        print("RAW DOCUMENT")
        print("=" * 100)

        for page in document.pages:

            print(

                f"Page {page.page_number} : "

                f"{len(page.layout_blocks)} Raw Blocks"

            )

        print("\n")
        print("=" * 100)
        print("AFTER LAYOUT NORMALIZATION")
        print("=" * 100)

        for page in document.pages:

            print(

                f"Page {page.page_number} : "

                f"{len(page.layout_blocks)} Normalized Blocks"

            )

        # ------------------------------------------------------
        # Layout Classification
        # ------------------------------------------------------

        print("\n")
        print("=" * 100)
        print("LAYOUT CLASSIFICATION")
        print("=" * 100)

        for page in document.pages:

            print(f"\nPAGE {page.page_number}")

            for block in page.layout_blocks:

                result = self.classifier.classify(

                    block

                )

                block.block_type = result.block_type

                block.classification_confidence = (

                    result.confidence

                )

                block.classification_reasons = (

                    result.reasons

                )

                print("\n" + "-" * 80)

                print(

                    f"BLOCK {block.block_number}"

                )

                print("-" * 80)

                print("TEXT")

                print(block.text)

                print()

                print(

                    f"TYPE        : {result.block_type}"

                )

                print(

                    f"CONFIDENCE  : {result.confidence}"

                )

                print(

                    f"REASONS     : {', '.join(result.reasons)}"

                )

                print(

                    f"BBOX        : {block.bbox}"

                )

                print(

                    f"LINES       : {block.line_count}"

                )

                print(

                    f"FONT SIZE   : {block.average_font_size:.2f}"

                )

                print(

                    f"BOLD        : {block.has_bold_text}"

                )

        # ------------------------------------------------------
        # Detect Sections
        # ------------------------------------------------------

        sections = self.section_detector.detect(document)

        print("\n")
        print("=" * 100)
        print("BUSINESS SECTIONS")
        print("=" * 100)

        print(f"Detected : {len(sections)}")

        for section in sections:

            print("\n" + "-" * 80)

            print(f"TITLE : {section.title}")

            print(f"PAGE  : {section.page_number}")

            print(f"BLOCKS: {len(section.blocks)}")

            print()

            print(section.text)
        # ------------------------------------------------------
        # Build Business Parameters
        # ------------------------------------------------------

        parameters = self.parameter_extractor.extract(

            sections

        )

        print("\n")
        print("=" * 100)
        print("BUSINESS PARAMETERS")
        print("=" * 100)

        print(

            f"Generated : {len(parameters)}"

        )

        for parameter in parameters:

            print("\n" + "-" * 80)

            print(parameter.name)

            print()

            print(parameter.value)

        # ------------------------------------------------------
        # Extraction Summary
        # ------------------------------------------------------

        print("\n")
        print("=" * 100)
        print("EXTRACTION SUMMARY")
        print("=" * 100)

        print(f"Pages      : {len(document.pages)}")
        print(f"Sections   : {len(sections)}")
        print(f"Parameters : {len(parameters)}")
        
        return parameters
    
