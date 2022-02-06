from DataExtraction.DocumentExtraction import DocumentExtraction
from Helpers.ConfigHelper import ConfigHelper
import GrobidWrapper.grobid_client as grobid
from Helpers.DirHelper import DirHelper
import shutil
import os

class DocumentHelper:
    
    @staticmethod
    def GetDocument(path):
        temp_folder = ConfigHelper.GetValue("DumpFolder")
        DirHelper.CreateDir(temp_folder)
        DirHelper.CleanDir(temp_folder)

        if (ConfigHelper.GetTextExtractionRules("PreprocessPDF")):
            DocumentExtraction.ParseText(path)
        else:
            shutil.move(path, temp_folder)

        client = grobid.grobid_client(config_path="./config.json")
        client.process("processFulltextDocument", temp_folder , output=temp_folder, consolidate_citations=True, teiCoordinates=True, force=True)
        
        for (dirpath, dirnames, filenames) in os.walk(temp_folder):
            for filename in filenames:
                if filename.endswith('.tei.xml'):
                    doc = DocumentExtraction.GetDocument(os.sep.join([dirpath, filename]))

        return doc

    @staticmethod
    def GetDocumentFromTEI():
        temp_folder = ConfigHelper.GetValue("DumpFolder")

        for (dirpath, dirnames, filenames) in os.walk(temp_folder):
            for filename in filenames:
                if filename.endswith('.tei.xml'):
                    doc = DocumentExtraction.GetDocument(os.sep.join([dirpath, filename]))

        return doc