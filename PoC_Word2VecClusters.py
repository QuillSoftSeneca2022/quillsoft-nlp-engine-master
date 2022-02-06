from gensim.models import word2vec
from DataClasses.Document import Document
from Summarization.SpacyHelper import SpacyHelper
from nltk import ngrams
from nltk import everygrams
from Extensions.QSString import QSString
import os

#label clusters with closest(fastext) phrase
def words_to_ngrams(sentence, n):
    grams = list(everygrams(sentence.split(), 1, n))
    words = []
    for g in grams:
        w = QSString((' '.join(g)))
        words.append(w.RemovePunctuation().strip().lower())
    return words

# vocabulary of the document to evaluate
def get_vocab():
    f = open("./test_files/test_input/12papers3.json", "r")
    doc = Document.from_json(f.read())

    words = []
    for block in doc.blocks:
        for paragraph in block.paragraphs:
            for sentence in paragraph:
                text = SpacyHelper.PreproccesText(sentence, True)
                tokens = text.split()
                words = words + tokens

    #remove duplicates
    words = list(dict.fromkeys(words))
    
    return words

# training data
sentences = []
for (dirpath, dirnames, filenames) in os.walk('./test_files/test_input/'):
    for filename in filenames:
        if filename.startswith('12papers'):
            f = open(os.sep.join([dirpath, filename]), "r")
            doc = Document.from_json(f.read())
            # define training data
            for block in doc.blocks:
                for paragraph in block.paragraphs:
                    for sentence in paragraph:
                        text = SpacyHelper.PreproccesText(sentence, True)
                        sentences.append(words_to_ngrams(text, 1))

# Set values for various parameters
feature_size = 100    # Word vector dimensionality  
window_context = 30          # Context window size                                                                                    
min_word_count = 1   # Minimum word count                        
sample = 1e-3   # Downsample setting for frequent words

# training model
w2v_model = word2vec.Word2Vec(sentences, size=feature_size, 
                          window=window_context, min_count=min_word_count,
                          sample=sample, iter=50)

concepts = ['cell','flu rna segment','flu shot','flu strain','h1n1 flu recover','h1n1 virus','h1n1','human','infected person','influenza virus','live virus','main surface antigen','novel swine flu','novel virus particle','novel','people','pig','predictable flu strain','respiratory','rna virus','rna','swine flu strain','swine flu virus','swine influenza virus','type','virus particle']
keyclusters = []
#tokenize phrases to single words.
for c in concepts:
    keyclusters += c.split()

#remove duplicates
keyclusters = list(dict.fromkeys(keyclusters))

# view similar words based on gensim's model
similar_words = {search_term: [item[0] for item in w2v_model.wv.most_similar([search_term], topn=30)]
                  for search_term in keyclusters}

concept_clusters = {}
vocab = get_vocab()
for concept in concepts:
    words = []
    for key in similar_words:
        if key in concept:
            words += similar_words[key]
    #remove duplicates
    words = list(dict.fromkeys(words))
    #remove words that don't belong to the article
    article_words = []
    for word in words:
        if word in vocab:
            article_words.append(word)
    concept_clusters[concept] = sorted(article_words)

print(concept_clusters)

for key in concept_clusters:
    print("{};{}".format(key, concept_clusters[key]))