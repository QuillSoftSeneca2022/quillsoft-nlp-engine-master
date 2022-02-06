import json

class ConfigHelper:

    with open('config.json') as config_file:
        _data = json.load(config_file)

    @property
    def data(self):
        return type(self)._data

    @data.setter
    def data(self,val):
        type(self)._data = val

    @classmethod
    def GetConfigValues(cls):
        instance = cls()
        result = {}
        result["SentencesByParagraph"] = instance.data["SentencesByParagraph"]
        result["PreprocessPDF"] = instance.data["TextExtractionRules"]["PreprocessPDF"]
        
        result["TextrankRatio"] = instance.data["TextSummarization"]["TextrankRatio"]
        result["SummSimilarityThreshold"] = instance.data["TextSummarization"]["SimilarityThreshold"]
        result["Lemma"] = instance.data["TextSummarization"]["Lemma"]

        result["PhrasesPercentage"] = instance.data["PhraseExtraction"]["PhrasesPercentage"]
        result["TopKeyPhrasesCount"] = instance.data["PhraseExtraction"]["TopKeyPhrasesCount"]
        result["PhraseSimilarityThreshold"] = instance.data["PhraseExtraction"]["SimilarityThreshold"]
        result["NGrams"] = instance.data["PhraseExtraction"]["NGrams"]
        lemma = instance.data["PhraseExtraction"]["Normalize"]
        result["Normalize"] = True if lemma == "lemma" else False

        return result

    @classmethod
    def SetConfigValues(cls, newvalues):
        instance = cls()
        
        with open('config.json', 'r') as infile:
            config_data = json.load(infile)
            
        config_data["SentencesByParagraph"] = int(newvalues["SentencesByParagraph"])
        config_data["TextExtractionRules"]["PreprocessPDF"] = newvalues["PreprocessPDF"]
        
        config_data["TextSummarization"]["TextrankRatio"] = float(newvalues["TextrankRatio"])
        config_data["TextSummarization"]["SimilarityThreshold"] = float(newvalues["SummSimilarityThreshold"])
        config_data["TextSummarization"]["Lemma"] = newvalues["Lemma"]

        config_data["PhraseExtraction"]["PhrasesPercentage"] = int(newvalues["PhrasesPercentage"])
        config_data["PhraseExtraction"]["TopKeyPhrasesCount"] = int(newvalues["TopKeyPhrasesCount"])
        config_data["PhraseExtraction"]["SimilarityThreshold"] = float(newvalues["PhraseSimilarityThreshold"])
        config_data["PhraseExtraction"]["NGrams"] = int(newvalues["NGrams"])
        lemma = "lemma" if newvalues["Normalize"] == True else "lower"
        config_data["PhraseExtraction"]["Normalize"] = lemma

        with open('config.json', 'w') as outfile:
            json.dump(config_data, outfile)
    
    @classmethod
    def ReloadFile(cls):
        instance = cls()
        with open('config.json') as config_file:
            instance.data = json.load(config_file)

    @classmethod
    def GetTextExtractionRules(cls, key):
        instance = cls()
        return instance.data["TextExtractionRules"][key]

    @classmethod
    def GetTextTranslationRules(cls, key):
        instance = cls()
        return instance.data["TextTranslation"][key]
        
    @classmethod
    def GetValue(cls, key):
        instance = cls()
        return instance.data[key]

    @classmethod
    def GetSummarizationValue(cls, key):
        instance = cls()
        return instance.data["TextSummarization"][key]

    @classmethod
    def GetPhraseExtractionValue(cls, key):
        instance = cls()
        return instance.data["PhraseExtraction"][key]