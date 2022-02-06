import math
import numpy as np
from typing import List
from dataclasses import dataclass, field
from DataClasses.Paragraph import Paragraph
from Helpers.ConfigHelper import ConfigHelper

@dataclass
class Block:
    title : str = None
    sequence : str = None
    paragraphs : List[str] = field(default_factory=List)

    #Splits a long paragraph into small paragraphs of n sentences.
    def TokenizeParagraphs(self):
        """
        :param self:
        :returns: list of paragraphs in text format
        """
        tokenized_list = []
        for paragraph in self.paragraphs:
            maxSentences = ConfigHelper.GetValue("SentencesByParagraph")
            length = len(paragraph)
            if (length > maxSentences):
                #TODO move this code to List Helper
                split_num = math.ceil(length / maxSentences)
                newparagraphs = np.array_split(paragraph, split_num)
                for p in newparagraphs:
                    tokenized_list.append(' '.join(p))
            else:
                tokenized_list.append(' '.join(paragraph))
        return tokenized_list

    #Splits a long paragraph into small paragraphs of n sentences.
    def TokenizeSentences(self):
        """
        :param self:
        :returns: list of paragraphs in sentences list format.
        """
        tokenized_list = []
        t_paragraphs = []
        for paragraph in self.paragraphs:
            sentences = []
            maxSentences = ConfigHelper.GetValue("SentencesByParagraph")
            length = len(paragraph)
            if (length > maxSentences):
                #TODO move this code to List Helper
                split_num = math.ceil(length / maxSentences)
                newparagraphs = np.array_split(paragraph, split_num)
                for p in newparagraphs:
                    t_paragraphs.append(p.tolist())
            else:
                t_paragraphs.append(paragraph)
        return t_paragraphs