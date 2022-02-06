from typing import List
from dataclasses import dataclass, field
from DataClasses.QSection import QSection
from dataclasses_json import dataclass_json

@dataclass_json
@dataclass
class QDocument:
    title: str = None
    abstract: str = None
    sections: List[QSection] = field(default_factory=list)
    detailedSummary: List[str] = field(default_factory=list)
    topViewSummary: List[str] = field(default_factory=list)
    concepts: List[str] = field(default_factory=list)