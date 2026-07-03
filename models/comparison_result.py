from dataclasses import dataclass
from models.business_change import BusinessChange
from models.business_analysis import BusinessAnalysis


@dataclass
class ComparisonResult:

    change: BusinessChange

    analysis: BusinessAnalysis