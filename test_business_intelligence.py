from models.business_change import BusinessChange

from ai.business_intelligence_engine import BusinessIntelligenceEngine


def main():

    change = BusinessChange(

        parameter="Minimum Maturity Age",

        matched_parameter="Minimum Maturity Age",

        source_version=1,

        target_version=2,

        old_value="18",

        new_value="20",

        change_type="VALUE_CHANGE",

        difference_text="18 → 20",

        old_text="""
Minimum Maturity Age : 18 Years
""",

        new_text="""
Minimum Maturity Age : 20 Years
"""

    )

    engine = BusinessIntelligenceEngine()

    analysis = engine.analyze(change)

    print("\n==============================")
    print(" BUSINESS ANALYSIS ")
    print("==============================\n")

    print(f"Summary               : {analysis.summary}")

    print(f"Business Impact       : {analysis.business_impact}")

    print(f"Affected Teams        : {analysis.affected_teams}")

    print(f"Risk                  : {analysis.risk}")

    print(f"Priority              : {analysis.priority}")

    print(f"Business Criticality  : {analysis.business_criticality_score}")

    print(f"Migration Impact      : {analysis.migration_impact}")

    print(f"Compliance Review     : {analysis.compliance_review}")

    print(f"Actuarial Review      : {analysis.actuarial_review}")

    print(f"Testing               : {analysis.testing_recommendations}")

    print(f"Recommendations       : {analysis.recommendations}")


if __name__ == "__main__":

    main()