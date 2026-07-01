from config.ai_config import SIMILARITY_THRESHOLD

class ParameterComparator:

    def compare(
        self,
        documents,
        repository
    ):
        """
        Performs semantic comparison between
        consecutive document versions using E5 embeddings.
        """

        comparison_table = []

        # ----------------------------------------
        # Compare V1->V2, V2->V3, V3->V4 ...
        # ----------------------------------------

        for i in range(len(documents) - 1):

            source = documents[i]
            target = documents[i + 1]

            # ----------------------------------------
            # Compare every parameter in source
            # ----------------------------------------

            for parameter, source_text in source["parameters"].items():

                best_match = repository.find_best_match(

                    source_parameter=parameter,

                    source_version=source["version"],

                    target_version=target["version"]

                )

                similarity = best_match["similarity"]

                row = {

                    # -----------------------------
                    # Version Information
                    # -----------------------------

                    "Source Version": source["version"],

                    "Target Version": target["version"],

                    # -----------------------------
                    # Parameter Mapping
                    # -----------------------------

                    "V1 Parameter": parameter,

                    "Matched V2 Parameter": best_match["parameter"],

                    "Similarity": similarity,

                    "Match Type": "Semantic",

                    # -----------------------------
                    # Parameter Content
                    # -----------------------------

                    "V1": source_text,

                    "V2": best_match["text"],

                    # -----------------------------
                    # Business Fields
                    # -----------------------------

                    "Business Category": "",

                    "Business Reason": ""

                }

                # ----------------------------------------
                # Determine Status
                # ----------------------------------------

                if similarity >= SIMILARITY_THRESHOLD:

                    row["Status"] = "Matched"

                    row["Business Reason"] = (
                        f"Semantic similarity {similarity:.2f}%."
                    )

                else:

                    row["Status"] = "Review Required"

                    row["Business Reason"] = (
                        f"Similarity below threshold ({similarity:.2f}%)."
                    )

                comparison_table.append(row)

        return comparison_table