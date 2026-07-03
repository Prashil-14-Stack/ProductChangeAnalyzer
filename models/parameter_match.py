@dataclass
class ParameterMatch:

    source_parameter: BusinessParameter

    matched_parameter: BusinessParameter

    confidence: float

    confidence_band: str

    status: str

    match_type: str