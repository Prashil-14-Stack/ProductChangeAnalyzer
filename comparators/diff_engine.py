import difflib


class DiffEngine:

    def compare_text(self, old_text, new_text):

        old_words = old_text.split()

        new_words = new_text.split()

        diff = difflib.ndiff(
            old_words,
            new_words
        )

        added = []
        removed = []

        for item in diff:

            if item.startswith("+ "):
                added.append(item[2:])

            elif item.startswith("- "):
                removed.append(item[2:])

        return {

            "Added":
                " ".join(added),

            "Removed":
                " ".join(removed)
        }