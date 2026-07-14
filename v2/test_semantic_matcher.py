"""
==========================================================
Semantic Matcher Test

Purpose
-------
Tests semantic matching independently of the
comparison engine.

==========================================================
"""

from comparison.semantic_matcher import SemanticMatcher
from models.business_parameter import BusinessParameter


def create_parameter(
    name,
    value="",
    category="General",
    section="General"
):

    return BusinessParameter(
        name=name,
        value=value,
        category=category,
        section=section
    )


def run_test(
    test_name,
    source,
    candidates
):

    print()
    print("=" * 80)
    print(test_name)
    print("=" * 80)

    matcher = SemanticMatcher()

    result = matcher.find_best_match(
        source,
        candidates
    )

    if result is None:

        print("No Match Found")

        return

    print()

    print("Best Match")

    print("-----------------------------")

    print(f"Parameter  : {result['parameter'].name}")

    print(f"Confidence : {result['confidence']}")

    print(f"Reason     : {result['reason']}")


def main():

    # ======================================================
    # Test 1
    # ======================================================

    source = create_parameter(

        "PPT",

        value="10 Years",

        category="Payment",

        section="Premium"
    )

    candidates = [

        create_parameter(

            "Policy Term",

            category="Policy",

            section="Policy"

        ),

        create_parameter(

            "Premium Payment Term",

            value="10 Years",

            category="Payment",

            section="Premium"

        ),

        create_parameter(

            "Premium Frequency",

            category="Payment",

            section="Premium"

        )

    ]

    run_test(

        "TEST 1 : PPT",

        source,

        candidates

    )

    # ======================================================
    # Test 2
    # ======================================================

    source = create_parameter(

        "Maximum Maturity Age",

        category="Age",

        section="Eligibility"

    )

    candidates = [

        create_parameter(

            "Minimum / Maximum Maturity Age",

            category="Age",

            section="Eligibility"

        ),

        create_parameter(

            "Policy Term"

        )

    ]

    run_test(

        "TEST 2 : Maturity Age",

        source,

        candidates

    )

    # ======================================================
    # Test 3
    # ======================================================

    source = create_parameter(

        "Death Benefit during PT",

        category="Benefits",

        section="Benefits"

    )

    candidates = [

        create_parameter(

            "Death Benefit",

            category="Benefits",

            section="Benefits"

        ),

        create_parameter(

            "Surrender Benefit",

            category="Benefits",

            section="Benefits"

        )

    ]

    run_test(

        "TEST 3 : Death Benefit",

        source,

        candidates

    )

    # ======================================================
    # Test 4
    # ======================================================

    source = create_parameter(

        "Completely New Parameter"

    )

    candidates = [

        create_parameter(

            "Death Benefit"

        ),

        create_parameter(

            "Premium Frequency"

        )

    ]

    run_test(

        "TEST 4 : No Match",

        source,

        candidates
    )


if __name__ == "__main__":

    main()