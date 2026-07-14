class InsuranceDictionary:
    """
    Enterprise Insurance Dictionary

    Maintains a vocabulary of common insurance
    business terms used during parameter extraction.
    """

    def __init__(self):

        self.terms = {

            # Product
            "policy",
            "premium",
            "sum",
            "assured",
            "coverage",
            "benefit",
            "maturity",
            "death",
            "survival",
            "surrender",
            "revival",
            "loan",
            "grace",
            "nominee",
            "assignment",
            "rider",
            "bonus",

            # Ages
            "entry",
            "minimum",
            "maximum",
            "age",

            # Terms
            "policy term",
            "premium payment term",
            "ppt",
            "pt",

            # Payment
            "annual",
            "monthly",
            "quarterly",
            "half yearly",
            "frequency",

            # Charges
            "gst",
            "tax",
            "charge",
            "charges",

            # Insurance Domain
            "ulip",
            "annuity",
            "claim",
            "risk",
            "underwriting",
            "mortality",
            "actuarial",
            "compliance"

        }

    def is_known_term(self, term: str) -> bool:

        return term.lower().strip() in self.terms