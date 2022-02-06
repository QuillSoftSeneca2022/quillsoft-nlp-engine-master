from typing import List
from dataclasses import dataclass, field
from DataClasses.QParagraph import QParagraph

@dataclass
class QSection:
    title : str = None
    sequence : str = None
    paragraphs : List[QParagraph] = field(default_factory=List)
    detailedSummary: List[str] = field(default_factory=List)
    topViewSummary: List[str] = field(default_factory=List)
    concepts: List[str] = field(default_factory=List)