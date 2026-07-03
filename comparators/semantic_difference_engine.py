from difflib import SequenceMatcher
import re


class SemanticDifferenceEngine:

    """
    Enterprise Business Change Extraction Engine

    Produces:
        • Difference text
        • Structured edit operations
        • Rich formatting segments
        • Added text
        • Removed text
        • Change classification
    """

    def compare(self, old_text, new_text):

        old_text = (old_text or "").strip()
        new_text = (new_text or "").strip()

        if old_text == new_text:

            return {

                "status": "No Change",

                "change_type": "NO_CHANGE",

                "difference_text": "",

                "segments": [],

                "operations": [

                    {
                        "type": "KEEP",
                        "text": old_text
                    }

                ],

                "added_text": [],

                "removed_text": []

            }

        # ----------------------------------------------------
        # Word Tokenization
        # ----------------------------------------------------

        old_tokens = re.findall(r"\S+", old_text)
        new_tokens = re.findall(r"\S+", new_text)

        matcher = SequenceMatcher(

            None,

            old_tokens,

            new_tokens

        )

        operations = []

        segments = []

        added_text = []

        removed_text = []

        difference_parts = []

        # ----------------------------------------------------
        # Build Edit Operations
        # ----------------------------------------------------

        for tag, i1, i2, j1, j2 in matcher.get_opcodes():

            # ==========================================
            # KEEP
            # ==========================================

            if tag == "equal":

                text = " ".join(old_tokens[i1:i2])

                operations.append({

                    "type": "KEEP",

                    "text": text

                })

            # ==========================================
            # ADD
            # ==========================================

            elif tag == "insert":

                text = " ".join(new_tokens[j1:j2])

                operations.append({

                    "type": "ADD",

                    "text": text

                })

                added_text.append(text)

                difference_parts.append(text)

                segments.append({

                    "text": text,

                    "type": "added",

                    "color": "green",

                    "bold": True

                })

            # ==========================================
            # DELETE
            # ==========================================

            elif tag == "delete":

                text = " ".join(old_tokens[i1:i2])

                operations.append({

                    "type": "DELETE",

                    "text": text

                })

                removed_text.append(text)

                difference_parts.append(

                    f"{text} (Removed)"

                )

                segments.append({

                    "text": text,

                    "type": "removed",

                    "color": "red",

                    "bold": True,

                    "strike": True

                })

            # ==========================================
            # REPLACE
            # ==========================================

            elif tag == "replace":

                old_part = " ".join(old_tokens[i1:i2])

                new_part = " ".join(new_tokens[j1:j2])

                operations.append({

                    "type": "REPLACE",

                    "old": old_part,

                    "new": new_part

                })

                added_text.append(new_part)

                removed_text.append(old_part)

                difference_parts.append(

                    f"{old_part} → {new_part}"

                )

                segments.append({

                    "type": "modified",

                    "previous": old_part,

                    "text": new_part,

                    "color": "green",

                    "bold": True

                })

        # ----------------------------------------------------
        # Determine Change Type
        # ----------------------------------------------------

        operation_types = {

            op["type"]

            for op in operations

        }

        if operation_types == {"ADD"}:

            change_type = "ADDITION"

        elif operation_types == {"DELETE"}:

            change_type = "DELETION"

        elif "REPLACE" in operation_types:

            change_type = "VALUE_CHANGE"

        elif "ADD" in operation_types:

            change_type = "CLAUSE_ADDED"

        elif "DELETE" in operation_types:

            change_type = "CLAUSE_REMOVED"

        else:

            change_type = "MODIFIED"

        return {

            "status": "Modified",

            "change_type": change_type,

            "difference_text": "\n".join(

                difference_parts

            ),

            "operations": operations,

            "segments": segments,

            "added_text": added_text,

            "removed_text": removed_text

        }