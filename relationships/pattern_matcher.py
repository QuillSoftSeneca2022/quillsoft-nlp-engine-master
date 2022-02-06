from spacy.matcher import Matcher
from abc import abstractmethod
from spacy.tokens import Doc
from relationships.relation import Relation


class PatternMatcher:


    def __init__(self, pattern, nlp, matcherId):
        self._nlp = nlp
        self._matcher = Matcher(nlp.vocab)
        self._matcher.add(matcherId, [pattern])

    @abstractmethod
    def getRelations(self, doc: Doc) -> [Relation]:
        ...
