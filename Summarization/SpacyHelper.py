import sys
import math
import spacy
import pytextrank
import textacy.ke
from spacy.attrs import ORTH
from string import punctuation
from collections import Counter
from spacy.matcher import Matcher
from Extensions.QSList import QSList
from Extensions.QSString import QSString
from Helpers.ConfigHelper import ConfigHelper
from Summarization.EnumMethods import EnumMethods
from Summarization.GensimHelper import GensimHelper


class SpacyHelper:
    # Load spacy model
    nlp = spacy.load(ConfigHelper.GetSummarizationValue("SpacyModel"))

    # add PyTextRank into the spaCy pipeline
    nlp.add_pipe("textrank", last=True)

    @classmethod
    def PreproccesText(cls, content, lemma=True):
        instance = cls()
        # Filter out stopwords
        text = GensimHelper.RemoveStopWords(content.lower().strip())
        text = QSString(text)
        # Remove punctuations
        text = text.RemovePunctuation()
        # Lemmatize each document - https://universaldependencies.org/docs/u/pos/
        pos_list = ConfigHelper.GetValue("SpacyUPOStags")
        if (lemma):
            text = ' '.join([token.lemma_ for token in instance.nlp(str(text)) if token.pos_ in pos_list])
        else:
            text = ' '.join([token.text for token in instance.nlp(str(text)) if token.pos_ in pos_list])
        return text

    @classmethod
    # Creates a summary of provided array
    def SummarizeArray(cls, arr):
        """
        :param arr: array of string - an array of sentences
        :returns: array of strings
        """
        instance = cls()
        p_len = len(arr)
        new_p = " ".join(arr)

        ratio = ConfigHelper.GetSummarizationValue("TextrankRatio")

        # Cannot summarize 1 sentence, just return this sentence
        if p_len == 1:
            return [new_p]

        # Adjust ratio depending on length of array (# of sentences), we want a minimum of 1 sentence
        if p_len * ratio < 1:
            ratio = 1 / p_len

        doc = instance.nlp(new_p)

        summarized = []
        num_sentences = round(ratio * p_len)

        # Summarize the document based on the top 15 phrases
        # TODO: calculate this value or move it to configuration file
        for sent in doc._.textrank.summary(limit_phrases=15, limit_sentences=num_sentences):
            summarized.append(sent.text)

        return summarized

    @classmethod
    # Takes the provided texts and returns an array of sentences
    def TokenizeSentences(cls, text):
        """
        :param text: plain text
        :return: array of strings
        """
        instance = cls()
        doc = instance.nlp(str(text))

        # Create list of sentence tokens
        sents_list = []
        for sent in doc.sents:
            #remove newlines and empty sentences
            text = sent.text.replace("\n", "").strip()
            if text != '' and len(text) > 3:
                sents_list.append(' '.join(text.split()))

        return sents_list

    @classmethod
    # Obtain the common top phrases (highest to lowest score) by performing Textacy Skip-Gram keyword extraction and Textacy Textrank keyword extraction on provided sentences
    # Testing with document level
    def GetConcepts(cls, sentences, document=False, sections=[]):
        """
        :param sentences: array of sentences for the keywords to be extracted
        :return: array of keywords(strings)
        """
        instance = cls()
        text = " ".join(sentences)
        #text = instance.preprocces_text(text)
        doc = instance.nlp(text.lower())

        # Percentage of phrases
        percent_phrases = ConfigHelper.GetPhraseExtractionValue("PhrasesPercentage")
        # Max number of words in a concept
        ngram = ConfigHelper.GetPhraseExtractionValue("NGrams")
        # If “lemma”, lemmatize words before counting; if “lower”, lowercase words before counting;
        normalize = ConfigHelper.GetPhraseExtractionValue("Normalize")
        # Calculate phrases count
        total_token = len(doc.count_by(ORTH))
        top_phrases_count = math.ceil((percent_phrases * total_token) / 100)

        # Get Concepts with Textrank keyword extraction
        top_tr_phrases = instance.ExtractConcepts(doc, top_phrases_count, document, ngram, normalize, EnumMethods.TEXTACY_TEXTRANK)
        # Get Concepts with Skip Gram keyword extraction
        top_sg_phrases = instance.ExtractConcepts(doc, top_phrases_count, document, ngram, normalize, EnumMethods.TEXTACY_SGRANK)

        # Perform list comprehension to find common key phrases and return the list
        top_tr_phrases = QSList(top_tr_phrases)
        if document:
            top_phrases = top_tr_phrases.MergeDocumentSentences(top_sg_phrases)
        else:
            top_phrases = top_tr_phrases.MergeSentences(top_sg_phrases)

        # This part is reserved for getting concepts at the document level
        if len(sections) > 0:
            top_phrases = instance.TuneDocumentConcepts(sections, top_phrases)

        return top_phrases

    @classmethod
    #Get back a list of concepts by applying the Concept Extraction Method selected
    def ExtractConcepts(cls, doc, top_phrases_count, document, ngram, normalize, method):
        instance = cls()
        if method == EnumMethods.TEXTACY_TEXTRANK:
            return instance.GetTextRankConcepts(doc, top_phrases_count, document, ngram, normalize)
        elif method == EnumMethods.TEXTACY_SGRANK:
            return instance.GetSkipGramConcepts(doc, top_phrases_count, document, ngram, normalize)

    @classmethod
    # Perform Textrank keyword extraction, returning keyphrases 1-4 words long
    def GetTextRankConcepts(cls, doc, top_phrases_count, document, ngram, normalize):
        top_tr_phrases = []
        tr_keywords = textacy.ke.textrank(doc, normalize=normalize, topn=top_phrases_count,)
        for trk in tr_keywords:
            # Filters keywords with periods in keywords and keywords larger than ngram words, textrank does not have ngrams parameter
            if "." not in trk[0] and len(trk[0].split()) <= ngram:
                if document:
                    top_tr_phrases.append(trk)
                else:
                    top_tr_phrases.append(trk[0])
        return top_tr_phrases

    @classmethod
    # Perform Skip Gram keyword extraction, returning keyphrases 1-ngram words long
    def GetSkipGramConcepts(cls, doc, top_phrases_count, document, ngram, normalize):
        
        #tuple of ngrams
        ngrams = ()
        for x in range(ngram):
            ngrams = ngrams + ( x + 1,)

        top_sg_phrases = []
        sg_keywords = textacy.ke.sgrank(doc, ngrams=ngrams, normalize=normalize, topn=top_phrases_count)
        for k in sg_keywords:
            if "." not in k[0]:
                if document:
                    top_sg_phrases.append(k)
                else:
                    top_sg_phrases.append(k[0])
        return top_sg_phrases

    @classmethod
    # Remove redundancies of document concepts based on section concepts
    def TuneDocumentConcepts(cls, sections, top_phrases):
        instance = cls()
        candidate_phrases = []
        final_concepts = []
        # Top_phrases should be an array of tuples(string, float). Tokenize the string in the tuple and append to list of candidate phrases with their score
        for phrase in top_phrases:
            t = (instance.nlp(phrase[0]), phrase[1])
            candidate_phrases.append(t)

        similarity = ConfigHelper.GetPhraseExtractionValue("SimilarityThreshold")

        # Compare each top_phrase to all concepts at section level, if they're a certain threshold(similarity) append them to final_list
        for sections in sections:
            # Tokenize concepts in sections
            for c in sections.concepts:
                token = instance.nlp(c)
                for cp in candidate_phrases:
                    if cp[0].similarity(token) > similarity:
                        final_concepts.append((cp[0].text, t[1]))

        # Remove duplicates and sort by descending order
        final_concepts = list(dict.fromkeys(final_concepts))
        sorted_final_concepts = sorted(final_concepts, key=lambda x: x[1], reverse=True)
        # Only retrieve the string from the tuple(string, float) of each list/array of tuples
        # If rank is also required, the MatchPhrases function will have to be tweaked at the document level
        final_concepts_list = [concepts[0] for concepts in sorted_final_concepts]

        return final_concepts_list

    @classmethod
    def ClusterPhrases(cls, phrase, phrases):
        """
        :param phrase: 
        :param phrases: array of phrases
        :returns: dictionary
        """
        instance = cls()
        final_phrases = []
        candidate_phrases = []
        token = instance.nlp(phrase)

        # Top_phrases should be an array of tuples(string, float). Tokenize the string in the tuple and append to list of candidate phrases with their score
        for p in phrases:
            t = (instance.nlp(p[0]), p[1])
            candidate_phrases.append(t)

        for p in candidate_phrases:
            similarity = p[0].similarity(token)
            if similarity > 0.1:
                final_phrases.append({p[0].text, round(similarity, 5)})

        return final_phrases

    @classmethod
    #Get base word
    def GetLemma(cls, word):
        instance = cls()
        return " ".join([token.lemma_ for token in instance.nlp(word)])

    @classmethod
    #Get the list of POS Tag within a phrase.
    def GetPOSTag(cls, phrase):
        instance = cls()
        doc = instance.nlp(phrase)
        result = []
        for token in doc:
            result.append(token.pos_)
        return result