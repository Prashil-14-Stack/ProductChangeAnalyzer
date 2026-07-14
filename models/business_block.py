from dataclasses import dataclass, field


@dataclass
class BusinessBlock:
    """
    ==========================================================
    Enterprise Business Block

    Represents one logical business section extracted
    from a Product Specification.

    Example

    Plan Description
        ↓
        Paragraph
        Paragraph
        Bullet List

    ==========================================================
    """

    # ---------------------------------------------------------
    # Identity
    # ---------------------------------------------------------

    parameter_name: str = ""

    # ---------------------------------------------------------
    # Content
    # ---------------------------------------------------------

    paragraphs: list[str] = field(default_factory=list)

    bullet_lists: list[str] = field(default_factory=list)

    tables: list = field(default_factory=list)

    notes: list[str] = field(default_factory=list)

    # ---------------------------------------------------------
    # Source
    # ---------------------------------------------------------

    page_number: int = 0

    source_blocks: list[int] = field(default_factory=list)

    # ---------------------------------------------------------
    # Confidence
    # ---------------------------------------------------------

    confidence: float = 0.0

    metadata: dict = field(default_factory=dict)

    # ==========================================================
    # Helpers
    # ==========================================================

    @property
    def description_text(self) -> str:

        return "\n".join(self.paragraphs)

    @property
    def has_tables(self):

        return len(self.tables) > 0

    @property
    def has_bullets(self):

        return len(self.bullet_lists) > 0

    def add_paragraph(self, text: str):

        text = text.strip()

        if text:

            self.paragraphs.append(text)

    def add_bullet(self, text: str):

        text = text.strip()

        if text:

            self.bullet_lists.append(text)

    def add_table(self, table):

        self.tables.append(table)

    def add_note(self, text: str):

        text = text.strip()

        if text:

            self.notes.append(text)

    def summary(self):

        return {

            "parameter": self.parameter_name,

            "paragraphs": len(self.paragraphs),

            "bullets": len(self.bullet_lists),

            "tables": len(self.tables),

            "notes": len(self.notes),

            "page": self.page_number,

            "confidence": self.confidence

        }