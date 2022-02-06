from PDFUtils.PyMuPDFParser import PyMuPDFParser
from Extensions.QSString import QSString
from Extensions.QSList import QSList
import re
import os


class PDFParser:
    
    ''' Gets raw text '''
    @staticmethod
    def GetParagraphs(path):
        cleanBlocks = []
        doc = PyMuPDFParser(path)
        pages = doc.GetPageCount()
        prevline = ''
        for pageNumber in range(pages):
            blocks = doc.GetBlocks(pageNumber)
            blocks = QSList(blocks).JoinHyphenatedBlocks()
            for block in blocks:
                text = QSString(block)
                text = text.RemoveElement(). \
                FixContractions(). \
                CheckElement(). \
                CheckWorthContent(). \
                CheckNumeric(). \
                CheckWhiteList(). \
                CheckBlackList(). \
                RemoveSpacesPunctuation(). \
                RemoveNumberPeriod(). \
                RemoveBullets(). \
                CheckHeading(prevline)
                if text != '-EMPTY-':
                    cleanBlocks.append(text.JoinHyphenatedLines())
                    prevline = text

        return QSList(cleanBlocks).JoinHyphenatedParagraphs()

    ''' Gets raw text filtered by font size '''
    @staticmethod
    def GetRawParagraphs(path):
        cleanBlocks = []
        doc = PyMuPDFParser(path)
        pages = doc.GetPageCount()
        avgSize = doc.GetAvgSize()
        for pageNumber in range(pages):
            blocks = doc.GetRawBlocks(pageNumber)
            for block in blocks:
                chunk = []
                for line in block['lines']:
                    for span in line['spans']:
                        if span['size'] >= avgSize:
                            chunk.append(span['text'])

                text = QSString(''.join(chunk))
                if (not text.IsPageNumber()):
                    cleanBlocks.append(text.JoinHyphenatedLines())

        return QSList(cleanBlocks).JoinHyphenatedParagraphs()
