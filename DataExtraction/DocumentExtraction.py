import os
import pdfkit
from PDFUtils.PDFParser import PDFParser
from DataExtraction.TEIFile import TEIFile
from DataClasses.Document import Document
from DataClasses.Block import Block
from DataClasses.Person import Person
from Extensions.QSString import QSString
from Helpers.ConfigHelper import ConfigHelper
from DataClasses.Paragraph import Paragraph
from Summarization.SpacyHelper import SpacyHelper

class DocumentExtraction:
    @staticmethod
    def ParseText(path):
        doc = PDFParser.GetParagraphs(path)
        temp_folder = ConfigHelper.GetValue("DumpFolder")
        file  = open(temp_folder + "temp_extraction.txt", "w", encoding="utf8", newline='') 
        for p in doc.value:
            file.write(p + "\n")
        file.close

        with open(temp_folder + "temp_extraction.txt", encoding="utf8",newline='') as file:
            with open (temp_folder + "temp_extraction.html", "w", encoding="utf8",newline='') as output:
                file = file.read()
                file = file.replace("\n", "<br>")
                output.write(file)
        
        path_wkhtmltopdf = ConfigHelper.GetValue("PDFKitExecutablePath")
        config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
        pdfkit.from_file(temp_folder + "temp_extraction.html", temp_folder + "temp_extraction.pdf", configuration=config)

    @staticmethod
    def GetDocument(path):
        tei = TEIFile(path)
        body = tei.body

        blocks = []
        sequence = ''
        title = ''
        for div in body:
            secuence = None
            paragraphs = []
            if len(div.find_all('head')) > 0:
                title = div.find_all('head')[0]
                if title.has_attr('n'):
                    sequence = title['n']
                title = title.text
            for p in div.find_all('p'):
                text = QSString(p.text)
                sentences = SpacyHelper.TokenizeSentences(text.RemoveElement().RemoveSpacesPunctuation())
                paragraphs.append(sentences)
            blocks.append(Block(title, sequence, paragraphs))

        abstract = QSString(tei.abstract)
        doc = Document(tei.title, abstract.RemoveElement().FormatNumbers().RemoveSpacesPunctuation().FixSymbols(), tei.authors, blocks)
        return doc

    @staticmethod
    def GetDocumentSentences(path):
        result = []
        blocks = PDFParser.GetParagraphs(path)
        for b in blocks.value:
            sentences = SpacyHelper.TokenizeSentences(b)
            result = result + sentences
        return result

    @staticmethod
    def GetDocumentText(path):
        blocks = PDFParser.GetParagraphs(path)
        return blocks
        