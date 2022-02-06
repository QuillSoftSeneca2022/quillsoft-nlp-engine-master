from Summarization.SpacyHelper import SpacyHelper
from Summarization.GensimHelper import GensimHelper
from Summarization.TFIDFHelper import TFIDFHelper
from Summarization.EnumMethods import EnumMethods
from Helpers.ConfigHelper import ConfigHelper
from DataClasses.QParagraph import QParagraph
from DataClasses.QDocument import QDocument
from DataClasses.QSection import QSection
from Extensions.QSString import QSString
from Extensions.QSList import QSList
import numpy as np


class QSummarization:

    doc = None
    corpus = []

    def __init__(self, doc):
        self.doc = doc
        # Initialize the corpus
        corpus = []
        for block in doc.blocks:
            for sentences in block.TokenizeParagraphs():
                corpus.append(sentences)
        self.corpus = corpus

    # Summarization pipeline, summarizes the sentences at paragraph, section, and document level
    def SummarizeDocument(self):
        # Create an empty QDocument object
        qdoc = QDocument(self.doc.title, self.doc.abstract, [], [], [], [])
        doc_sentences = []
        for block in self.doc.blocks:
            block_sentences = []

            # Create a Qsection object
            section = QSection(block.title, block.sequence, [], [], [], [])
            for paragraphs in block.TokenizeSentences():
                block_sentences += paragraphs
                section_result = self.SummarizeSections(paragraphs)

                # Create a QParagraph and append it to the section paragraphs array
                section.paragraphs.append(
                    QParagraph(section_result[0], section_result[1], section_result[2])
                )
            doc_sentences += block_sentences

            # Get back summaries and concept arrays and assign them to the section
            section_result = self.SummarizeSections(block_sentences)
            section.detailedSummary = section_result[0]
            section.topViewSummary = section_result[1]
            section.concepts = section_result[2]
            qdoc.sections.append(section)

        # Get back summaries and concept arrays and assign them to the document
        section_result = self.SummarizeSections(doc_sentences, True, qdoc.sections)
        qdoc.detailedSummary = section_result[0]
        qdoc.topViewSummary = section_result[1]
        qdoc.concepts = section_result[2]
        return qdoc

    # Gets an array with the result of the detailedSummary, topViewSummary and concepts
    def SummarizeSections(self, sentences, isDocLevel=False, sections=[]):
        """
        :param self:
        :param sentences: array of text sentences
        :param isDocLevel: flag that indicates summary belongs to document level
        :param sections: array of sections of the document
        """
        if len(sentences) > 0:
            # Remove numbers and symbols to apply similarity filter
            fixed_sentences = []
            for sentence in sentences:
                if ConfigHelper.GetSummarizationValue("Lemma"):
                    fixed_sentences.append(SpacyHelper.PreproccesText(sentence))
                else:
                    text = QSString(sentence)
                    fixed_sentences.append(GensimHelper.RemoveStopWords(text.FormatNumbers().FixSymbols().lower()))
                
            result = []
            # Similarity filter
            filtered_sentences = TFIDFHelper.tfidf(
                self.corpus,
                fixed_sentences,
                ConfigHelper.GetSummarizationValue("SimilarityThreshold"),
            )
            # array of numpy sentences
            array = np.array(fixed_sentences)
            # array of numpy original sentences
            oarray = np.array(sentences)
            # Get indexes of summarized sentence with Spacy
            sentence_indexes1 = self.SummarizeText(
                filtered_sentences, array, EnumMethods.SPACY_TEXTRANK
            )
            # Get indexes of summarized sentences with gensim
            sentence_indexes2 = self.SummarizeText(
                filtered_sentences, array, EnumMethods.GENSIM
            )

            # Total of sentences of both summaries removing duplicates and sorted
            # Detailed Summary
            sentence_indexes = QSList(sentence_indexes1).MergeSentences(sentence_indexes2)
            result.append(oarray[sentence_indexes].tolist())
            # Matched/sorted sentences in both summaries
            # Top View Summary
            sentence_indexes = QSList(sentence_indexes1).JoinSentences(sentence_indexes2)
            result.append(oarray[sentence_indexes].tolist())
            # Concepts
            concepts = SpacyHelper.GetConcepts(result[0], isDocLevel, sections)
            result.append(concepts)
            return result
        else:
            return [[], [], []]

    # Gets back the summarized array of sentences based on the summarization method applied
    def SummarizeText(self, sentences, osentences, method):
        """
        :param self:
        :param sentences: array of sentences to be summarized
        :param osentences: array of sentences before summarization and similarity filter
        :param method: summarization method to be applied
        :returns: list of indexes where the chosen sentences are.
        """
        # list of indexes with the position of the summarized sentences on the original array
        index_list = []

        if method == EnumMethods.SPACY_TEXTRANK:
            summarized_sentences = SpacyHelper.SummarizeArray(sentences)
        elif method == EnumMethods.GENSIM:
            summarized_sentences = GensimHelper.SummarizeArray(sentences)

        for sentence in summarized_sentences:
            # Get the index of the matching sentence
            matching = [s for s in sentences if sentence in s]
            if len(matching) > 0:
                index_list += np.where(osentences == matching[0])[0].tolist()
            else:
                for index, text in np.ndenumerate(osentences):
                    if text in sentence:
                        index_list += index

        return index_list
