from typing import List
from dataclasses import dataclass, field

@dataclass
class QParagraph:
    detailedSummary: List[str] = field(default_factory=List)
    topViewSummary: List[str] = field(default_factory=List)
    concepts: List[str] = field(default_factory=List)