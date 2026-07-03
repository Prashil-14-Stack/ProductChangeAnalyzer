"""
==============================================================

Product Change Analyzer V2.0

Life Insurance Business Dictionary

This file contains all standard business terminology used
across the Product Change Analyzer.

Every module should reference this dictionary instead of
hardcoding insurance terms.

==============================================================
"""


# ==========================================================
# PRODUCT ELIGIBILITY
# ==========================================================

ELIGIBILITY_TERMS = [

    "Minimum Entry Age",
    "Maximum Entry Age",
    "Minimum Maturity Age",
    "Maximum Maturity Age",
    "Policy Term",
    "Premium Paying Term",
    "Premium Payment Term",
    "Entry Age",
    "Maturity Age",
    "Age at Entry",
    "Age at Maturity"

]


# ==========================================================
# PREMIUM
# ==========================================================

PREMIUM_TERMS = [

    "Premium",
    "Annual Premium",
    "Modal Premium",
    "Single Premium",
    "Regular Premium",
    "Limited Premium",
    "Premium Frequency",
    "Premium Payment Frequency",
    "Premium Mode",
    "Loading",
    "Discount"

]


# ==========================================================
# BENEFITS
# ==========================================================

BENEFIT_TERMS = [

    "Death Benefit",
    "Maturity Benefit",
    "Survival Benefit",
    "Guaranteed Benefit",
    "Guaranteed Addition",
    "Loyalty Addition",
    "Terminal Bonus",
    "Cash Value",
    "Fund Value",
    "Sum Assured",
    "Basic Sum Assured",
    "Benefit"

]


# ==========================================================
# SURRENDER
# ==========================================================

SURRENDER_TERMS = [

    "Surrender",
    "Surrender Value",
    "Guaranteed Surrender Value",
    "Special Surrender Value",
    "Paid-up",
    "Paid Up",
    "Revival",
    "Grace Period",
    "Free Look",
    "Free Look Cancellation"

]


# ==========================================================
# RIDERS
# ==========================================================

RIDER_TERMS = [

    "Accidental Death Benefit Rider",
    "Critical Illness Rider",
    "Waiver of Premium Rider",
    "Hospital Cash Rider",
    "Term Rider",
    "Rider"

]


# ==========================================================
# CLAIMS
# ==========================================================

CLAIMS_TERMS = [

    "Claim",
    "Death Claim",
    "Maturity Claim",
    "Partial Withdrawal",
    "Settlement Option"

]


# ==========================================================
# NOMINATION
# ==========================================================

NOMINATION_TERMS = [

    "Nominee",
    "Nomination",
    "Assignment",
    "Appointee"

]


# ==========================================================
# TAX
# ==========================================================

TAX_TERMS = [

    "GST",
    "TDS",
    "Tax",
    "Income Tax",
    "Section 80C",
    "Section 10(10D)"

]


# ==========================================================
# COMPLIANCE
# ==========================================================

COMPLIANCE_TERMS = [

    "IRDAI",
    "AML",
    "KYC",
    "FATCA",
    "Regulatory"

]


# ==========================================================
# PAYMENTS
# ==========================================================

PAYMENT_TERMS = [

    "ECS",
    "NACH",
    "Auto Debit",
    "Credit Card",
    "Debit Card",
    "Net Banking",
    "UPI",
    "Cheque",
    "Standing Instruction"

]


# ==========================================================
# COMMON BUSINESS PHRASES
# ==========================================================

BUSINESS_PHRASES = [

    "For POS Channel",
    "For Online Channel",
    "For Agency Channel",
    "For Broker Channel",

    "Single Life",
    "Joint Life",

    "Policyholder",
    "Life Assured",
    "Nominee",

    "Policy Anniversary",

    "Issue Date",

    "Risk Commencement Date"

]


# ==========================================================
# MASTER LIST
# ==========================================================

ALL_BUSINESS_TERMS = sorted(

    list(

        set(

            ELIGIBILITY_TERMS

            + PREMIUM_TERMS

            + BENEFIT_TERMS

            + SURRENDER_TERMS

            + RIDER_TERMS

            + CLAIMS_TERMS

            + NOMINATION_TERMS

            + TAX_TERMS

            + COMPLIANCE_TERMS

            + PAYMENT_TERMS

            + BUSINESS_PHRASES

        )

    ),

    key=len,

    reverse=True

)