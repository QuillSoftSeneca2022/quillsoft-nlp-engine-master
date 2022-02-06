from typing import List
from dataclasses import dataclass, field
from DataClasses.Person import Person
from DataClasses.Block import Block
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Document:
    title: str = None
    abstract: str = None
    autors: List[Person] = field(default_factory=List)
    blocks: List[Block] = field(default_factory=List)

