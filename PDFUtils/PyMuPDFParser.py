import fitz
from PDFUtils.PDFPage import PDFPage
from collections import Counter

class PyMuPDFParser:
    doc = None
    pdfpage = None

    def __init__(self, path):
        self.doc = fitz.open(path)

    def GetPageCount(self):
        return self.doc.pageCount

    def GetAvgSize(self):
        fontSize = []
        for pageNumber in range(self.GetPageCount()):
            page = self.doc[pageNumber]
            blocks = page.getText("dict", flags=0)["blocks"]

            for block in blocks:
                for line in block['lines']:
                    for span in line['spans']:
                        fontSize.append(span['size'])
        sizeDict = Counter(fontSize)
        avg = max(sizeDict.keys(), key=(lambda key: sizeDict[key]))
        return avg

    def GetBlocks(self, pageNumber):
        result = []
        page = self.doc[pageNumber]
        blocks = page.getText('blocks')
        for block in blocks:
            result.append(block[4])
        return result

    def GetRawBlocks(self, pageNumber):
        result = []
        page = self.doc[pageNumber]
        blocks = page.getText("dict", flags=0)["blocks"]
        return blocks

    def GetText(self, pageNumber):
        page = self.doc[pageNumber]
        ppage = PDFPage(page.getText(), pageNumber + 1, 'text')
        return ppage

    def SearchText(self, text):
        frequency = []
        for pageNumber in range(self.GetPageCount()):
            count = 0
            page = self.doc[pageNumber]
            matches = page.searchFor(text)
            count += len(matches)
            p = {"page": pageNumber + 1, "count": count }
            frequency.append(p)
        return frequency