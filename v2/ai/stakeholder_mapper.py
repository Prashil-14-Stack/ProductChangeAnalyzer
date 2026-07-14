"""
==========================================================
Stakeholder Mapper

Purpose
-------
Identifies stakeholders impacted by product changes.

Responsibilities
----------------
✓ Identify Responsible Teams
✓ Identify Approvers
✓ Identify Reviewers
✓ Generate Stakeholder Matrix

This module is deterministic and rule-based.

==========================================================
"""


class StakeholderMapper:

    # ======================================================
    # Constructor
    # ======================================================

    def __init__(self):

        self.rules = {

            "benefit": [

                "Product Team",

                "Business Analyst",

                "QA",

                "Actuarial",

                "Compliance"

            ],

            "death": [

                "Product Team",

                "QA",

                "Actuarial",

                "Compliance"

            ],

            "maturity": [

                "Product Team",

                "QA",

                "Actuarial"

            ],

            "premium": [

                "Finance",

                "Product Team",

                "QA"

            ],

            "eligibility": [

                "Business Analyst",

                "Product Team",

                "QA",

                "Compliance"

            ],

            "age": [

                "Business Analyst",

                "QA",

                "Compliance"

            ],

            "policy": [

                "Operations",

                "QA",

                "Product Team"

            ],

            "option": [

                "Operations",

                "Customer Service",

                "QA"

            ],

            "frequency": [

                "Operations",

                "QA"

            ],

            "loan": [

                "Operations",

                "Finance"

            ],

            "tax": [

                "Compliance",

                "Finance"

            ],

            "surrender": [

                "Operations",

                "QA",

                "Compliance"

            ]

        }

    # ======================================================
    # Public
    # ======================================================

    def map(
        self,
        comparison_result
    ):

        stakeholders = {}

        for item in comparison_result.items:

            if item.status.lower() == "unchanged":

                continue

            parameter = item.parameter_name.lower()

            teams = set()

            for keyword, mapped_teams in self.rules.items():

                if keyword in parameter:

                    teams.update(mapped_teams)

            if not teams:

                teams.add(

                    "Business Analyst"

                )

            stakeholders[item.parameter_name] = {

                "status": item.status,

                "impact": item.impact,

                "teams": sorted(

                    list(teams)

                )

            }

        return stakeholders

    # ======================================================
    # Summary
    # ======================================================

    def summarize(
        self,
        stakeholder_map
    ):

        summary = {}

        for parameter in stakeholder_map.values():

            for team in parameter["teams"]:

                summary.setdefault(

                    team,

                    0

                )

                summary[team] += 1

        return dict(

            sorted(

                summary.items(),

                key=lambda x: x[1],

                reverse=True

            )

        )