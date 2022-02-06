from typing import List
from dataclasses import dataclass, field

@dataclass
class Paragraph:
    osentences: List[str] = field(default_factory=List)
    fsentences: List[str] = field(default_factory=List)