"""
==========================================================
Layout Graph

Represents the complete document layout as a graph.

Nodes
-----
LayoutObjects

Edges
-----
LayoutRelationships

This graph becomes the central knowledge base used by:

    • TableStructureBuilder
    • SectionBuilder
    • BusinessParameterExtractor
    • AI Analyzer

==========================================================
"""

from dataclasses import dataclass, field
from collections import defaultdict
from typing import List, Dict

from legacy.pdf_engine_v1.core.models.layout_relationship import (
    LayoutRelationship,
    RelationshipType
)


@dataclass
class LayoutGraph:
    """
    Graph of document layout.
    """

    # --------------------------------------------------
    # Graph Nodes
    # --------------------------------------------------

    nodes: List = field(default_factory=list)

    # --------------------------------------------------
    # Graph Edges
    # --------------------------------------------------

    relationships: List[LayoutRelationship] = field(
        default_factory=list
    )

    # --------------------------------------------------
    # Internal Index
    # --------------------------------------------------

    adjacency: Dict[int, List[LayoutRelationship]] = field(
        default_factory=lambda: defaultdict(list)
    )

    # ==================================================
    # Node Management
    # ==================================================

    def add_node(self, node):

        if node not in self.nodes:

            self.nodes.append(node)

    # ==================================================
    # Relationship Management
    # ==================================================

    def add_relationship(
        self,
        relationship: LayoutRelationship
    ):

        self.relationships.append(relationship)

        if relationship.source is not None:

            self.adjacency[
                id(relationship.source)
            ].append(relationship)

    # ==================================================
    # Query Relationships
    # ==================================================

    def get_relationships(self, node):

        return self.adjacency.get(id(node), [])

    # --------------------------------------------------

    def get_relationships_of_type(

        self,

        node,

        relationship_type: RelationshipType

    ):

        return [

            r

            for r in self.get_relationships(node)

            if r.relationship_type == relationship_type

        ]

    # ==================================================
    # Convenience Queries
    # ==================================================

    def get_neighbors(self, node):

        return [

            r.target

            for r in self.get_relationships(node)

        ]

    # --------------------------------------------------

    def get_same_row(self, node):

        return [

            r.target

            for r in self.get_relationships_of_type(

                node,

                RelationshipType.SAME_ROW

            )

        ]

    # --------------------------------------------------

    def get_same_column(self, node):

        return [

            r.target

            for r in self.get_relationships_of_type(

                node,

                RelationshipType.SAME_COLUMN

            )

        ]

    # --------------------------------------------------

    def get_below(self, node):

        return [

            r.target

            for r in self.get_relationships_of_type(

                node,

                RelationshipType.BELOW

            )

        ]

    # --------------------------------------------------

    def get_above(self, node):

        return [

            r.target

            for r in self.get_relationships_of_type(

                node,

                RelationshipType.ABOVE

            )

        ]

    # --------------------------------------------------

    def get_left(self, node):

        return [

            r.target

            for r in self.get_relationships_of_type(

                node,

                RelationshipType.LEFT_OF

            )

        ]

    # --------------------------------------------------

    def get_right(self, node):

        return [

            r.target

            for r in self.get_relationships_of_type(

                node,

                RelationshipType.RIGHT_OF

            )

        ]

    # ==================================================
    # Statistics
    # ==================================================

    @property
    def node_count(self):

        return len(self.nodes)

    @property
    def relationship_count(self):

        return len(self.relationships)

    # ==================================================
    # Debug
    # ==================================================

    def summary(self):

        print("\n")
        print("=" * 100)
        print("LAYOUT GRAPH")
        print("=" * 100)

        print(f"Nodes         : {self.node_count}")
        print(f"Relationships : {self.relationship_count}")

    # ==================================================
    # Representation
    # ==================================================

    def __str__(self):

        return (

            f"LayoutGraph("

            f"nodes={self.node_count}, "

            f"relationships={self.relationship_count})"

        )

    __repr__ = __str__