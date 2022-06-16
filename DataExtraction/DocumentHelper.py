from DataExtraction.DocumentExtraction import DocumentExtraction
from Helpers.ConfigHelper import ConfigHelper
import GrobidWrapper.grobid_client as grobid
from Helpers.DirHelper import DirHelper
import shutil
import os
from datetime import datetime
import requests
#from Controllers.SummarizationController import send_api

class DocumentHelper:

    def send_api(path, method): 
        API_HOST = "http://localhost:7000" 
        url = API_HOST + path 
        headers = {'Accept': 'application/xml'} 
        #body 
        body = {'key1': 'value1', 'key2': 'value2' }

        try: 
            if method == 'GET': 
                print("get function works")
                response = requests.get(url, headers=headers) 
                #print("response status %r" % response.status_code) 
                #print("response text %r" % response.text) 
                return response.text
            elif method == 'POST': 
                headers = {"Content-Type": "multipart/form-data"}
                print("headers", headers)
                response = requests.post(url, headers=headers, data=json.dumps(body, ensure_ascii=False, indent="\t")) 
                print("response status %r" % response.status_code) 
                print("response text %r" % response.text) 
        except Exception as ex: 
            print(ex)

    @staticmethod
    def GetDocument(path):
        temp_folder = ConfigHelper.GetValue("DumpFolder")
        DirHelper.CreateDir(temp_folder)
        DirHelper.CleanDir(temp_folder)

        if (ConfigHelper.GetTextExtractionRules("PreprocessPDF")):
            DocumentExtraction.ParseText(path)
        else:
            shutil.move(path, temp_folder)

        #COMMENT OUT - GROBID part  
        #client = grobid.grobid_client(config_path="./config.json")
        #client.process("processFulltextDocument", temp_folder , output=temp_folder, consolidate_citations=True, teiCoordinates=True, force=True)
        #print("xml is generated and done",datetime.now())
        
        # for (dirpath, dirnames, filenames) in os.walk(temp_folder):
        #     for filename in filenames:
        #         # this is edited for test, beyond and should be deleted after the test.
        #         if filename.endswith('.tei.xml'):
        #             print("path name: ",os.sep.join([dirpath, filename]))
        #             doc = DocumentExtraction.GetDocument(os.sep.join([dirpath, filename]))
        print("start sending api", datetime.now())

        # send file to node js server 
        files = {'upload_file': open('./temp/input/input_file.pdf', 'rb')}
        requests.post("http://localhost:7000/api", files = files )
        # send tei request to node js server and get tei.xml file
        response = requests.get("http://localhost:7000/api/tei", headers={'Accept': 'application/xml'}) 
    
        # store it as file from returned data
        with open('./test_files/test.tei.xml', 'w') as f:
            data = response.text
            f.write(data)
        # set doc as new test file 
        doc = DocumentExtraction.GetDocument('./test_files/test.tei.xml')
        print("finish receiving api", datetime.now())
        return doc

    @staticmethod
    def GetDocumentFromTEI():
        temp_folder = ConfigHelper.GetValue("DumpFolder")

        for (dirpath, dirnames, filenames) in os.walk(temp_folder):
            for filename in filenames:
                if filename.endswith('.tei.xml'):
                    doc = DocumentExtraction.GetDocument(os.sep.join([dirpath, filename]))

        return doc

    