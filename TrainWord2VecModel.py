from gensim.models import Word2Vec
from gensim.utils import tokenize
from DataClasses.Document import Document
from dataclasses_json import dataclass_json
from nltk import ngrams
from Extensions.QSString import QSString
from Summarization.SpacyHelper import SpacyHelper

from nltk import everygrams
import os

def words_to_ngrams(sentence, n):
    grams = list(everygrams(sentence.split(), 1, n))
    words = []
    for g in grams:
        w = QSString((' '.join(g)))
        words.append(w.RemovePunctuation().strip().lower())
    return words

sentences = []

#Get text from 12papers
for (dirpath, dirnames, filenames) in os.walk('./test_files/test_input/'):
    for filename in filenames:
        if filename.startswith('12papers'):
            f = open(os.sep.join([dirpath, filename]), "r")
            doc = Document.from_json(f.read())
            # define training data
            for block in doc.blocks:
                for paragraph in block.paragraphs:
                    for sentence in paragraph:
                        text = SpacyHelper.PreproccesText(sentence, False)
                        sentences.append(words_to_ngrams(text, 3))

'''f = open("./test_files/test_input/12papers3.json", "r")
doc = Document.from_json(f.read())

for block in doc.blocks:
    for paragraph in block.paragraphs:
        for sentence in paragraph:
            text = SpacyHelper.PreproccesText(sentence, False)
            sentences.append(words_to_ngrams(text, 3))'''

# train model
#TODO Move constants to config file or calculate 
model = Word2Vec(sentences, min_count=1, size=10000, sg=1)
# save model
model.save('Models/model.bin')
