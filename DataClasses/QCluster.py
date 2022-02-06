from typing import List
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json

@dataclass_json
@dataclass
class QCluster:
    concept: str = None
    words: List[str] = field(default_factory=List)
    POSTags: List[str] = field(default_factory=List)
    closestConcept: str = None