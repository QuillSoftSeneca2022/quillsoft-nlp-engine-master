from gensim.summarization import summarize
from Helpers.ConfigHelper import ConfigHelper
from gensim.parsing.preprocessing import remove_stopwords
from gensim.summarization import keywords


class GensimHelper:
    @classmethod
    # Returns a string summary from provided array of strings
    def SummarizeArray(cls, arr):
        """
        :param arr: array of string - an array of sentences
        :return: array of strings
        """
        p_len = len(arr)
        text = " ".join(arr)

        # TODO move ratio to configuration file
        ratio = ConfigHelper.GetSummarizationValue("TextrankRatio")

        summarized = []

        # Cannot summarize less than 3 sentences
        if p_len < 3:
            for sentence in arr:
                summarized.append(sentence)
            return summarized

        # Adjust ratio depending on length of array (# of sentences), we want a minimum of 1 sentence
        if p_len * ratio < 1:
            ratio = 1 / p_len

        try:
            for sentence in summarize(text, ratio, None, True):
                summarized.append(sentence)
        except:
            # Gensim cannot summarize less than 2 sentences
            summarized.append(text)

        return summarized

    @classmethod
    # Removes stopwords from the text
    def RemoveStopWords(cls, text):
        """
        :param text:
        :returns: string
        """
        return remove_stopwords(text)

    @classmethod
    # Returns the top phrases in the provided sentences from highest score to lowest
    def GetKeyWords(cls, sentences):
        """
        :param sentences: array of sentences where the keywords need to be extracted
        :returns: array of strings
        """
        text = " ".join(sentences)
        return keywords(text).split("\n")

