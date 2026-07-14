"""
==========================================================
Enterprise Figure Detector

Purpose
-------
Detect non-text visual regions inside a document.

Current Version
---------------
Uses image metadata extracted by PDFReader.

Future Versions
---------------
✓ Diagram Detection
✓ Chart Detection
✓ Flow Detection
✓ Logo Detection
✓ Watermark Detection

==========================================================
"""

from legacy.pdf_engine_v1.core.models.figure_region import FigureRegion


class FigureDetector:

    # ======================================================
    # Process
    # ======================================================

    def process(self, document):

        document.figures = []

        for page in document.pages:

            figures = self._detect_figures(page)

            document.figures.extend(figures)

        return document

    # ======================================================
    # Detect Figures
    # ======================================================

    def _detect_figures(self, page):

        figures = []

        # -----------------------------------------------
        # Images extracted by PDFReader
        # -----------------------------------------------

        if not hasattr(page, "images"):

            return figures

        for image in page.images:

            figure = FigureRegion(

                page_number=page.page_number,

                bbox=image.get(

                    "bbox",

                    (0, 0, 0, 0)

                ),

                figure_type="IMAGE",

                confidence=0.90

            )

            figure.metadata = image

            figures.append(

                figure

            )

        return figures