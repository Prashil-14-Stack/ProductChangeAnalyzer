"""
==========================================================
Application Constants

Purpose
-------
Central location for application-wide constants.

These values should remain stable across environments.

Do NOT place runtime configuration here.
Those belong in settings.py.

==========================================================
"""

# ==========================================================
# Comparison Status
# ==========================================================

STATUS_ADDED = "Added"

STATUS_REMOVED = "Removed"

STATUS_MODIFIED = "Modified"

STATUS_UNCHANGED = "Unchanged"

STATUS_UNKNOWN = "Unknown"


# ==========================================================
# Parameter Sources
# ==========================================================

SOURCE_PDF = "PDF"

SOURCE_DOCX = "DOCX"

SOURCE_JSON = "JSON"

SOURCE_MANUAL = "MANUAL"


# ==========================================================
# Output File Names
# ==========================================================

COMPARISON_REPORT = "Comparison_Report.xlsx"

JSON_EXPORT = "Comparison_Result.json"

WORD_REPORT = "Comparison_Report.docx"


# ==========================================================
# Excel Sheet Names
# ==========================================================

SHEET_SUMMARY = "Summary"

SHEET_ADDED = "Added"

SHEET_REMOVED = "Removed"

SHEET_MODIFIED = "Modified"

SHEET_UNCHANGED = "Unchanged"

SHEET_AI_IMPACT = "AI Impact"


# ==========================================================
# GPT Response Keys
# ==========================================================

KEY_PRODUCT_NAME = "product_name"

KEY_PRODUCT_VERSION = "product_version"

KEY_DOCUMENT_TYPE = "document_type"

KEY_PARAMETERS = "parameters"

KEY_METADATA = "metadata"

KEY_PAGE_NUMBER = "page_number"

KEY_PARAMETER_NAME = "parameter_name"

KEY_PARAMETER_VALUE = "parameter_value"

KEY_CATEGORY = "category"


# ==========================================================
# Business Categories
# ==========================================================

CATEGORY_ELIGIBILITY = "Eligibility"

CATEGORY_POLICY = "Policy"

CATEGORY_PREMIUM = "Premium"

CATEGORY_BENEFITS = "Benefits"

CATEGORY_CHARGES = "Charges"

CATEGORY_RIDERS = "Riders"

CATEGORY_LOAN = "Loan"

CATEGORY_REVIVAL = "Revival"

CATEGORY_SURRENDER = "Surrender"

CATEGORY_CLAIMS = "Claims"

CATEGORY_TAX = "Tax"

CATEGORY_MISCELLANEOUS = "Miscellaneous"


# ==========================================================
# AI Analysis Sections
# ==========================================================

AI_BUSINESS_IMPACT = "Business Impact"

AI_RISK = "Risk Assessment"

AI_COMPLIANCE = "Compliance Impact"

AI_AFFECTED_TEAMS = "Affected Teams"

AI_TEST_CASES = "Suggested Test Cases"

AI_IMPLEMENTATION_NOTES = "Implementation Notes"


# ==========================================================
# Supported File Types
# ==========================================================

SUPPORTED_INPUT_TYPES = (
    ".pdf",
    ".docx"
)

SUPPORTED_OUTPUT_TYPES = (
    ".xlsx",
    ".json",
    ".docx"
)


# ==========================================================
# Comparison Types
# ==========================================================

COMPARE_EXACT = "Exact"

COMPARE_SEMANTIC = "Semantic"

COMPARE_AI = "AI Assisted"