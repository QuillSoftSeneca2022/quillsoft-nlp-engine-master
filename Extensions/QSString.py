import re
import string 
import contractions
from string import digits
from Helpers.ConfigHelper import ConfigHelper

class QSString (str):
    empty = '-EMPTY-'
    def __init__ (self, value):
        self.value = value

    def JoinHyphenatedLines (self):
        return re.sub(r'-\n|- \n(\w+ *)', r'\1\n', self.value)

    def RemoveElement(self):
        try:
            regex_list = ConfigHelper.GetTextExtractionRules("ElementsToRemove")
            expression = '(?:% s)' % '|'.join(regex_list) 
            return QSString(re.sub(expression, " ", self.value))
        except:
            return self

    def FixContractions(self):
        contraction_list = ConfigHelper().GetTextTranslationRules("CustomContractions")
        for key, value in contraction_list.items():
            contractions.add(key, value)
        return QSString(contractions.fix(self.value))

    def FixSymbols(self):
        dict = ConfigHelper().GetTextTranslationRules("CustomTranslations")[0]
        for key in dict:
            self.value = self.value.replace(key, "")
        return QSString(self.value)

    def RemoveSpacesPunctuation(self):
        #Remove spaces before puntuation
        return QSString(re.sub("\s*([?.,;](?:\s|$))", "\\1", self.value))

    def RemovePunctuation(self):
        #Remove spaces before puntuation
        return QSString(re.sub(r'[^a-zA-Z0-9-]', ' ', self.value))

    def RemoveNumberPeriod(self):
        #Remove numbers after period
        expression = "[A-Za-z]\.\d*[ \n\t]"
        tags = re.findall(expression, self.value)
        if len(tags) > 0:
            for tag in tags:
                replace_text = tag.translate(str.maketrans('', '', digits))
                self.value = self.value.replace(tag, replace_text)
            return QSString(self.value)
        else:
            return self

    def CheckElement(self):
        regex_list = ConfigHelper.GetTextExtractionRules("SectionsToRemove")
        expression = '(?:% s)' % '|'.join(regex_list) 
        return QSString(self.empty) if re.search(expression, self.value) else self

    def CheckWorthContent (self):
        alphaCount = len(re.findall('[a-zA-Z]', self.value))
        if alphaCount > 0:
            total = len(self.value)
            percentage = (alphaCount * 100) / total
            minPercentage = int(ConfigHelper.GetTextExtractionRules("MinAlphaInBlock"))
            return QSString(self.empty) if percentage < minPercentage else self
        else: 
            return self

    def CheckWhiteList (self):
        whiteList = ConfigHelper.GetTextExtractionRules("WhiteListHeadings")
        text = self.value.upper().translate(str.maketrans('','', ' \n\t\r'))
        return QSString(text) if text in whiteList else self

    def CheckBlackList (self):
        blackList = ConfigHelper.GetTextExtractionRules("BlackListWords")
        return QSString(self.empty) if (bool([ele for ele in blackList if(ele in self.value.upper())])) else self

    def CheckNumeric (self):
        #Remove numeric blocks
        text = self.value.translate(str.maketrans('','', ' \n\t\r,\.%-'))
        return QSString(self.empty) if text.isnumeric() else self

    def CheckHeading (self, prevline):
        #Add proper format to a heading
        try:
            return QSString(' \n' + self.value + '\n ') if self.value[0].isdigit() and self.value.isupper() and not prevline.isspace() else self
        except:
            return self

    def FormatNumbers(self):
        number_list = []
        words = re.split(' |-|/|%|\+|!|>|<', self.value)
        numbers = [ i for i in words if i.replace(',', '').replace('.', '').isdecimal() ]
        if len(numbers) > 0:
            for n in numbers:
                number = n.replace(',','').rstrip('.').rstrip(',')
                number = number.replace(".","") if number.count('.') > 1 else number
                f = float(number)
                number_list.append((f, n))

            number_list.sort(key=lambda tup: tup[1], reverse=True)

            for number in number_list:
                self.value = re.sub("(?<=\b|/|-|%|\+|!|>|<| )*" + number[1] + "(?=\b|/|-|%|\+|!|>|<| )*", "", self.value)
            return QSString(self.value)
        else:
            return self

    def RemoveBullets(self):
        #Remove bullets (4 spaces)
        return QSString(self.value.replace('    ',''))