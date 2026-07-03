from comparators.parameter_matcher import ParameterMatcher
from comparators.description_matcher import DescriptionMatcher
from comparators.change_detector import ChangeDetector
from comparators.decision_engine import DecisionEngine
from comparators.semantic_difference_engine import SemanticDifferenceEngine
from ai.business_intelligence_engine import BusinessIntelligenceEngine
from models.business_change import BusinessChange

class ParameterComparator:

    def __init__(self):

        self.parameter_matcher = ParameterMatcher()

        self.difference_engine = SemanticDifferenceEngine()

        self.description_matcher = DescriptionMatcher()

        self.change_detector = ChangeDetector()
        
        self.decision_engine = DecisionEngine()

        self.business_intelligence = BusinessIntelligenceEngine()

    # ==========================================================
    # Compare Documents
    # ==========================================================

    def compare(

        self,

        documents,

        repository

    ):

        comparison_table = []

        # ------------------------------------------------------
        # Compare V1→V2, V2→V3 ...
        # ------------------------------------------------------

        for i in range(len(documents) - 1):

            source = documents[i]

            target = documents[i + 1]

            # --------------------------------------------------
            # Compare every parameter
            # --------------------------------------------------

            for parameter in source.parameters:
                source_text = parameter.value

                # ----------------------------------------------
                # Retrieve Top-K Semantic Candidates
                # ----------------------------------------------

                candidates = repository.find_candidates(

                    source_parameter=parameter.name,

                    source_version=source.version,

                    target_version=target.version

                )
                parameter_result = self.parameter_matcher.match(

                    source_parameter=parameter.name,

                    source_description=source_text,

                    candidates=candidates

                )            
                matched_parameter = matched_parameter.name
                print("\n\n\n")
                print("************* DEBUG *************")
                print(f"Source Parameter: {parameter.name}")

                if not candidates:
                    print("NO CANDIDATES FOUND")
                else:
                    for i, c in enumerate(candidates, start=1):
                        print(
                            f"{i}. {c['parameter']} | {c['similarity']}%"
                        )

                print("********************************")
                print("\n\n\n")
                # ----------------------------------------------
                # No Match Found
                # ----------------------------------------------

                if parameter_result["status"] == "No Match":

                    comparison_table.append({

                        "Source Version": source.version,

                        "Target Version": target.version,

                        "V1 Parameter": parameter,

                        "Matched V2 Parameter": "NO MATCH FOUND",

                        "Parameter Confidence": parameter_result["confidence"],

                        "Confidence Band": parameter_result["confidence_band"],

                        "Description Confidence": 0,

                        "Overall Confidence": parameter_result["confidence"],

                        "Decision": "No Match",

                        "Status": "Added / Removed",

                        "V1": source_text,

                        "V2": "",

                        "Change Type": "New / Removed Parameter",

                        "Severity": "High",

                        "Remarks": "No semantically similar parameter found."

                    })

                    continue

                # ----------------------------------------------
                # Description Matching
                # ----------------------------------------------

                description_result = self.description_matcher.compare(

                    source_text,

                    matched_parameter.value

                )

                difference_result = self.difference_engine.compare(

                    old_text=source_text,

                    new_text=matched_parameter.value

                )
                # ----------------------------------------------
                # Business Change Object
                # ----------------------------------------------

                business_change = BusinessChange(

                    # ======================================================
                    # New Object-Oriented Model
                    # ======================================================

                    source_parameter=parameter,

                    target_parameter=matched_parameter,

                    # ======================================================
                    # Backward Compatibility
                    # ======================================================

                    parameter=parameter.name,

                    matched_parameter=matched_parameter.name,

                    source_version=source.version,

                    target_version=target.version,

                    old_value=source_text,

                    new_value=matched_parameter.value,

                    old_text=source_text,

                    new_text=matched_parameter.value,

                    difference_text=difference_result["difference_text"],

                    change_type=difference_result["change_type"]

                )
                # ----------------------------------------------
                # Business Intelligence
                # ----------------------------------------------

                analysis = self.business_intelligence.analyze(

                    business_change

                )
                remarks = analysis.summary
                # ----------------------------------------------
                # Change Detection
                # ----------------------------------------------

                change_result = self.change_detector.detect(

                    source_text,

                    matched_parameter.value,

                    description_result["confidence"]

                )

                # ----------------------------------------------
                # Final Decision
                # ----------------------------------------------

                decision = self.decision_engine.decide(

                    parameter_result,

                    description_result

                )

                # ----------------------------------------------
                # Overall Confidence
                # ----------------------------------------------

                overall_confidence = round(

                    (

                        parameter_result["confidence"] +

                        description_result["confidence"]

                    ) / 2,

                    2

                )

                # ----------------------------------------------
                # Final Row
                # ----------------------------------------------

                comparison_table.append({

                    "Source Version": source["version"],

                    "Target Version": target["version"],

                    "V1 Parameter": parameter.name,

                    "Matched V2 Parameter":

                        matched_parameter.name,

                    "Parameter Confidence":

                        parameter_result["confidence"],

                    "Confidence Band":

                        parameter_result["confidence_band"],

                    "Description Confidence":

                        description_result["confidence"],

                    "Overall Confidence":

                        overall_confidence,

                    "Decision":

                        decision["status"],

                    "Status":

                        decision["status"],

                    "V1":

                        source_text,

                    "V2":

                        matched_parameter.value,

                    "Difference":

                        difference_result["difference_text"],

                    "Difference Segments":
                        
                        difference_result["segments"],

                    "Change Type":

                        change_result["change_type"],

                    "Severity":

                        change_result["severity"],

                    "Remarks":

                        remarks,

                    "Summary":

                        analysis.summary,

                    "Business Impact":

                        analysis.business_impact,

                    "Affected Teams":

                        ", ".join(

                            analysis.affected_teams

                        ),

                    "Testing":

                        "\n".join(

                            analysis.testing_recommendations

                        ),

                    "Risk":

                        analysis.risk,

                    "Priority":

                        analysis.priority,

                    "Business Criticality":

                        analysis.business_criticality_score,

                })

        return comparison_table