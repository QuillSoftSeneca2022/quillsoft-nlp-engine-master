#source: https://programmerbackpack.com/python-knowledge-graph-understanding-semantic-relationships/

from relationships.and_other_pattern_matcher import AndOtherPatternMatcher
from relationships.such_as_pattern_matcher import SuchAsPatternMatcher
from relationships.or_other_pattern_matcher import OrOtherPatternMatcher
from relationships.including_pattern_matcher import IncludingPatternMatcher
from relationships.especially_pattern_matcher import EspeciallyPatternMatcher
from relationships.knowledge_graph import KnowledgeGraph
from relationships.matcher_pipe import MatcherPipe
import spacy
from DataExtraction.DocumentExtraction import DocumentExtraction

#load spacy model with sentencizer pipeline
nlp = spacy.load('en_core_web_md')
nlp.add_pipe('sentencizer', first=True) # updated

def draw_graph_sr(file_path):
    text = DocumentExtraction.GetDocumentSentences(file_path)

    sentences = ""
    for t in text:
        sentences += " " + t

    doc = nlp(sentences)

    andOtherPatternMatcher = AndOtherPatternMatcher(nlp)
    suchAsMatcher = SuchAsPatternMatcher(nlp)
    orOtherMatcher = OrOtherPatternMatcher(nlp)
    includingPatternMatcher = IncludingPatternMatcher(nlp)
    especiallyPatternMatcher = EspeciallyPatternMatcher(nlp)
    matcherPipe = MatcherPipe()
    matcherPipe.addMatcher(andOtherPatternMatcher)
    matcherPipe.addMatcher(suchAsMatcher)
    matcherPipe.addMatcher(orOtherMatcher)
    matcherPipe.addMatcher(includingPatternMatcher)
    matcherPipe.addMatcher(especiallyPatternMatcher)
    relations = matcherPipe.extract(doc)

    #for relation in relations:
    #    print (relation.getHypernym(), relation.getHyponym())

    knowledgeGraph = KnowledgeGraph(relations)
    knowledgeGraph.build()
    knowledgeGraph.show()
