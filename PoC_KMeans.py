from gensim.models import Word2Vec
 
from nltk.cluster import KMeansClusterer
import nltk
 
from sklearn import cluster
from sklearn import metrics

from DataClasses.Document import Document
from nltk import ngrams
from Extensions.QSString import QSString
from nltk import everygrams
from Summarization.SpacyHelper import SpacyHelper

import numpy as np


#return a list of n-grams from the given test
def words_to_ngrams(sentence, n):
    grams = list(everygrams(sentence.split(), 1, n))
    words = []
    for g in grams:
        w = QSString((' '.join(g)))
        words.append(w.RemovePunctuation().strip().lower())
    return words
 
# training data
f = open("./test_files/test_input/12papers3.json", "r")
doc = Document.from_json(f.read())

sentences = []

for block in doc.blocks:
    for paragraph in block.paragraphs:
        for sentence in paragraph:
            text = SpacyHelper.PreproccesText(sentence, True)
            #text = sentence
            sentences.append(words_to_ngrams(text, 1))
 
# training model
model = Word2Vec(sentences, min_count=1, sg=1)

#Save and Load model from the disk
#model.save('Models/model.bin')
#model = Word2Vec.load('Models/model.bin')

# get vector data
X = model[model.wv.vocab]

#26 is the number of key-phrases at document level.
NUM_CLUSTERS=26
kclusterer = KMeansClusterer(NUM_CLUSTERS, distance=nltk.cluster.util.euclidean_distance, repeats=25)
#kclusterer = KMeansClusterer(NUM_CLUSTERS, distance=nltk.cluster.util.cosine_distance, repeats=25)
assigned_clusters = kclusterer.cluster(X, assign_clusters=True)
 
#fit clusters in an array
clusters = [[]] * NUM_CLUSTERS
words = list(model.wv.vocab)
for i, word in enumerate(words):
    index = assigned_clusters[i]
    clusters[index] = clusters[index] + [word]

# train fasttext model for rarewords
from gensim.models import FastText
model = FastText(sentences, min_count=1, sg=1)

concepts = ['cell','flu rna segment','flu shot','flu strain','h1n1 flu recover','h1n1 virus','h1n1','human','infected person','influenza virus','live virus','main surface antigen','novel swine flu','novel virus particle','novel','people','pig','predictable flu strain','respiratory','rna virus','rna','swine flu strain','swine flu virus','swine influenza virus','type','virus particle']

#label clusters with closest(fastext) phrase
matched_concept = []
for concept in concepts:
    max_distance = 0
    concept_index = 0
    index = 0
    for cluster in clusters:
        total_distance = 0
        for word in cluster:
            total_distance += model.wv.similarity(concept, word)
        if total_distance > max_distance:
            max_distance = total_distance
            concept_index = index
        index = index + 1
    matched_concept.append((concept, concept_index))

for concept, index in matched_concept:
    print ("{},{}".format(concept, clusters[index]))

