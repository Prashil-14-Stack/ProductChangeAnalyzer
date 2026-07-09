"""
==========================================================
Knowledge Loader

Purpose
-------
Loads business knowledge used throughout the application.

Currently Supports
------------------
✓ Parameter aliases

Future
------
✓ Insurance glossary
✓ Business rules
✓ Impact rules
✓ Regulatory mappings

==========================================================
"""

from pathlib import Path

import yaml


class KnowledgeLoader:

    """
    Loads YAML-based business knowledge.
    """

    # ======================================================
    # Constructor
    # ======================================================

    def __init__(self, knowledge_folder=None):

        if knowledge_folder is None:

            knowledge_folder = (
                Path(__file__).resolve().parent
            )

        self.knowledge_folder = knowledge_folder

        self.alias_lookup = {}

        self.load_parameter_aliases()

    # ======================================================
    # Load Parameter Aliases
    # ======================================================

    def load_parameter_aliases(self):

        yaml_file = (
            self.knowledge_folder /
            "parameter_aliases.yaml"
        )

        if not yaml_file.exists():

            raise FileNotFoundError(

                f"Alias file not found:\n{yaml_file}"

            )

        with open(

            yaml_file,

            "r",

            encoding="utf-8"

        ) as file:

            aliases = yaml.safe_load(file)

        self.alias_lookup = {}

        for canonical_name, alias_list in aliases.items():

            canonical_key = self._normalize(
                canonical_name
            )

            # Canonical maps to itself

            self.alias_lookup[canonical_key] = canonical_name

            # Every alias maps to canonical

            for alias in alias_list:

                alias_key = self._normalize(alias)

                self.alias_lookup[alias_key] = canonical_name

    # ======================================================
    # Public
    # ======================================================

    def get_canonical_name(self, parameter_name):

        key = self._normalize(parameter_name)

        return self.alias_lookup.get(

            key,

            parameter_name

        )

    # ------------------------------------------------------

    def alias_exists(self, parameter_name):

        key = self._normalize(parameter_name)

        return key in self.alias_lookup

    # ------------------------------------------------------

    def total_aliases(self):

        return len(self.alias_lookup)

    # ======================================================
    # Helpers
    # ======================================================

    def _normalize(self, text):

        if not text:

            return ""

        return (

            str(text)

            .strip()

            .lower()

            .replace("-", " ")

            .replace("_", " ")

        )