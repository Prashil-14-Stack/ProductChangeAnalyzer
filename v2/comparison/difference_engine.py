"""
==========================================================
Difference Engine

Purpose
-------
Generates a human-readable business difference between
two parameter values.

==========================================================
"""

import re
from difflib import SequenceMatcher


class DifferenceEngine:

    # ======================================================
    # Public
    # ======================================================

    def compare(
        self,
        old_value,
        new_value
    ):

        old = self._clean(old_value)

        new = self._clean(new_value)

        if old == new:
            return "No Difference"

        messages = []

        # --------------------------------------------------
        # Numeric Changes
        # --------------------------------------------------

        numeric = self._numeric_changes(
            old,
            new
        )

        if numeric:
            messages.extend(numeric)

        # --------------------------------------------------
        # Added / Removed Text
        # --------------------------------------------------

        added, removed = self._text_changes(
            old,
            new
        )

        if added:

            messages.append("Added:")

            for text in added:

                messages.append(f"• {text}")

        if removed:

            messages.append("Removed:")

            for text in removed:

                messages.append(f"• {text}")

        # --------------------------------------------------
        # Minor wording changes
        # --------------------------------------------------

        if not messages:

            similarity = SequenceMatcher(
                None,
                old,
                new
            ).ratio()

            if similarity > 0.90:

                return "Minor wording changes"

            return f"{old}\n↓\n{new}"

        return "\n".join(messages)

    # ======================================================
    # Numeric Changes
    # ======================================================

    def _numeric_changes(
        self,
        old,
        new
    ):

        old_numbers = re.findall(r"\d+(?:\.\d+)?", old)

        new_numbers = re.findall(r"\d+(?:\.\d+)?", new)

        changes = []

        for old_num, new_num in zip(old_numbers, new_numbers):

            if old_num != new_num:

                changes.append(

                    f"Modified: {old_num} → {new_num}"

                )

        return changes

    # ======================================================
    # Text Changes
    # ======================================================

    def _text_changes(
        self,
        old,
        new
    ):

        matcher = SequenceMatcher(
            None,
            old.split(),
            new.split()
        )

        added = []

        removed = []

        for tag, i1, i2, j1, j2 in matcher.get_opcodes():

            if tag == "insert":

                text = " ".join(

                    new.split()[j1:j2]

                ).strip()

                if text:

                    added.append(text)

            elif tag == "delete":

                text = " ".join(

                    old.split()[i1:i2]

                ).strip()

                if text:

                    removed.append(text)

            elif tag == "replace":

                old_text = " ".join(

                    old.split()[i1:i2]

                ).strip()

                new_text = " ".join(

                    new.split()[j1:j2]

                ).strip()

                if old_text != new_text:

                    removed.append(old_text)

                    added.append(new_text)

        return added, removed

    # ======================================================
    # Clean
    # ======================================================

    def _clean(
        self,
        value
    ):

        if value is None:

            return ""

        value = str(value)

        value = value.replace("\r", " ")

        value = value.replace("\n", " ")

        value = re.sub(
            r"\s+",
            " ",
            value
        )

        return value.strip()