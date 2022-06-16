from gensim.models import word2vec
from gensim.utils import tokenize
from DataClasses.QCluster import QCluster
from dataclasses_json import dataclass_json
from Summarization.SpacyHelper import SpacyHelper
from nltk import ngrams
from Extensions.QSString import QSString
from nltk import everygrams
import json

class QClustering:

    doc_words = None

    '''def __init__(self):
        #initialize Word2Vec model
        #TODO: mode model path to config file
        self.model = word2vec.load('Models/model.bin')'''

    # Get related sentences
    def GetSentences(self, phrase, sentences):

        result = []
        for s in sentences:
            if phrase in s.lower():
                result.append(s)
        return result

    # Build clusters of phrases with Word2Vec method (Unigrams)
    def BuildClusters(self, sentences, phrases):

        clean_sentences = []
        doc_dict = []
        self.doc_words = []
        #Preprocces text
        for sentence in sentences:
            text = SpacyHelper.PreproccesText(sentence, False)
            ngrams = self.words_to_ngrams(text, 1)
            clean_sentences.append(ngrams)
            doc_dict = doc_dict + ngrams
            self.doc_words += ngrams

        # Set values for various parameters
        feature_size = 200    # Word vector dimensionality  
        window_context = 30          # Context window size                                                                                    
        min_word_count = 1   # Minimum word count                        
        sample = 1e-3   # Downsample setting for frequent words

        #Get word embedings model
        w2v_model = word2vec.Word2Vec(clean_sentences, size=feature_size, 
                                window=window_context, min_count=min_word_count,
                                sample=sample, iter=50)

        keyclusters = []
        #tokenize phrases
        for c in phrases:
            keyclusters += c.split()

        #remove duplicates
        keyclusters = list(dict.fromkeys(keyclusters))
        #remove words that are not part of the model
        clean_keyclusters = []
        for key in keyclusters:
            if key in doc_dict:
                clean_keyclusters.append(key)

        # get similar words based on gensim's model
        similar_words = {search_term: [item[0] for item in w2v_model.wv.most_similar([search_term], topn=30)]
                        for search_term in clean_keyclusters}

        phrase_clusters = {}
        for concept in phrases:
            words = []
            for key in similar_words:
                if key in concept:
                    words += similar_words[key]
            #remove duplicates
            words = list(dict.fromkeys(words))
            phrase_clusters[concept] = self.add_lemma(sorted(words))

        return phrase_clusters

    #Add base form(lemma) for a list of words
    def add_lemma(self, words):
        result = []
        for word in words:
            if len(word) > 2:
                lemma = SpacyHelper.GetLemma(word)
                frequency = self.doc_words.count(word)
                result.append([word, lemma, frequency])
        return result

    #Tokenize n-grams
    def words_to_ngrams(self, sentence, n):
        grams = list(everygrams(sentence.split(), 1, n))
        words = []
        for g in grams:
            w = QSString((' '.join(g)))
            words.append(w.RemovePunctuation().strip().lower())
        return words

    #get closest concept of a given one (single/compound) 
    def closest_concept(self, phrases, concept, wv_model):
        result = None
        closest = 0
        for c in phrases:
            avg = 0
            if (c != concept):
                #evaluate cosine distance within single words
                for cword in concept.split():
                    for word in c.split():
                        avg += wv_model.similarity(cword, word)
                avg = avg / (len(concept.split()) + len(c.split()))
                if avg > closest:
                    result = c
                    closest = avg
        return result