"""
==========================================================
Knowledge Loader

Purpose
-------
Loads the Insurance Knowledge Base.

Knowledge Files

business/
    knowledge/
        insurance_dictionary.yaml
        parameter_aliases.yaml

Provides APIs for

    ✓ Known parameter detection
    ✓ Alias lookup
    ✓ Category lookup
    ✓ Parameter normalization

==========================================================
"""

from pathlib import Path
import yaml


class KnowledgeLoader:

    def __init__(self):

        base_path = Path(__file__).parent / "knowledge"

        self.dictionary_path = (
            base_path / "insurance_dictionary.yaml"
        )

        self.alias_path = (
            base_path / "parameter_aliases.yaml"
        )

        self.categories = {}

        self.aliases = {}

        self.reverse_alias = {}

        self.load()

    # ======================================================
    # Load Knowledge Base
    # ======================================================

    def load(self):

        self._load_dictionary()

        self._load_aliases()

    # ======================================================
    # Insurance Dictionary
    # ======================================================

    def _load_dictionary(self):

        with open(

            self.dictionary_path,

            "r",

            encoding="utf-8"

        ) as file:

            self.categories = yaml.safe_load(file)

    # ======================================================
    # Parameter Aliases
    # ======================================================

    def _load_aliases(self):

        with open(

            self.alias_path,

            "r",

            encoding="utf-8"

        ) as file:

            self.aliases = yaml.safe_load(file)

        self.reverse_alias = {}

        for canonical, aliases in self.aliases.items():

            self.reverse_alias[

                canonical.lower()

            ] = canonical

            for alias in aliases:

                self.reverse_alias[

                    alias.lower()

                ] = canonical

    # ======================================================
    # Known Parameter
    # ======================================================

    def is_known_parameter(

        self,

        text

    ):

        return (

            text.lower()

            in

            self.reverse_alias

        )

    # ======================================================
    # Normalize
    # ======================================================

    def normalize(

        self,

        text

    ):

        return self.reverse_alias.get(

            text.lower(),

            text

        )

    # ======================================================
    # Category
    # ======================================================

    def get_category(

        self,

        parameter

    ):

        parameter = self.normalize(parameter)

        for category, values in self.categories.items():

            if parameter in values:

                return category

        return "Unknown"

    # ======================================================
    # Aliases
    # ======================================================

    def get_aliases(

        self,

        parameter

    ):

        parameter = self.normalize(parameter)

        return self.aliases.get(

            parameter,

            []

        )

    # ======================================================
    # All Parameters
    # ======================================================

    def all_parameters(self):

        parameters = []

        for values in self.categories.values():

            parameters.extend(values)

        return sorted(

            list(set(parameters))

        )

    # ======================================================
    # Debug
    # ======================================================

    def debug(self):

        print()

        print("=" * 100)

        print("KNOWLEDGE BASE")

        print("=" * 100)

        print()

        print(

            f"Categories : {len(self.categories)}"

        )

        print(

            f"Parameters : {len(self.all_parameters())}"

        )

        print(

            f"Aliases    : {len(self.reverse_alias)}"

        )

        print()

        for category in self.categories:

            print(

                f"{category} ({len(self.categories[category])})"

            )