from comparators.parameter_matcher import ParameterMatcher
from comparators.description_matcher import DescriptionMatcher
from comparators.change_detector import ChangeDetector
from comparators.decision_engine import DecisionEngine

from services.llm_service import LLMService


class ParameterComparator:

    def __init__(self):

        self.parameter_matcher = ParameterMatcher()

        self.description_matcher = DescriptionMatcher()

        self.change_detector = ChangeDetector()

        self.decision_engine = DecisionEngine()

        self.llm = LLMService()

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

            for parameter, source_text in source["parameters"].items():

                # ----------------------------------------------
                # Retrieve Top-K Semantic Candidates
                # ----------------------------------------------

                candidates = repository.find_candidates(

                    source_parameter=parameter,

                    source_version=source["version"],

                    target_version=target["version"]

                )
                parameter_result = self.parameter_matcher.match(

                    source_parameter=parameter,

                    source_description=source_text,

                    candidates=candidates

                )                
                print("\n\n\n")
                print("************* DEBUG *************")
                print(f"Source Parameter: {parameter}")

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

                        "Source Version": source["version"],

                        "Target Version": target["version"],

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

                    parameter_result["matched_text"]

                )

                # ----------------------------------------------
                # Change Detection
                # ----------------------------------------------

                change_result = self.change_detector.detect(

                    source_text,

                    parameter_result["matched_text"],

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
                # Remarks (GPT Stub)
                # ----------------------------------------------

                if decision["status"] == "No Change":

                    remarks = "No business impact."

                else:

                    remarks = self.llm.generate_remarks(

                        parameter,

                        source_text,

                        parameter_result["matched_text"],

                        decision=decision["status"]
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

                    "V1 Parameter": parameter,

                    "Matched V2 Parameter":

                        parameter_result["matched_parameter"],

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

                        parameter_result["matched_text"],

                    "Change Type":

                        change_result["change_type"],

                    "Severity":

                        change_result["severity"],

                    "Remarks":

                        remarks

                })

        return comparison_table