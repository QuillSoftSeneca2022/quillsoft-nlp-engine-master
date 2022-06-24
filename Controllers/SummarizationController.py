#region access to parent folder of the solution
import os
import sys
import requests
import json
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
#endregion

import json
from flask_cors import CORS
from flask import Flask, request
from werkzeug.utils import secure_filename
from Helpers.TestHelper import GetText
from Helpers.DirHelper import DirHelper
from Helpers.ConfigHelper import ConfigHelper
from Clustering.QClustering import QClustering
from Summarization.QSummarization import QSummarization
from DataExtraction.DocumentHelper import DocumentHelper
from DataExtraction.DocumentExtraction import DocumentExtraction
from datetime import datetime


app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

clustering = QClustering()
cache = {}

#region global functions

def upload_file(file):
    result = 'file uploaded successfully'
    try:
        if file.filename.endswith('.tei.xml'):
            uploads_folder = ConfigHelper.GetValue("DumpFolder")
            DirHelper.CreateDir(uploads_folder)
            DirHelper.CleanDir(uploads_folder)
            file.save(os.path.join(uploads_folder, secure_filename('input_file.tei.xml')))
            cache['filetype'] = 'tei'
            print('upload file function - tei.xml ')
        else:
            uploads_folder = ConfigHelper.GetValue("UploadsFolder")
            DirHelper.CreateDir(uploads_folder)
            file.save(os.path.join(uploads_folder, secure_filename('input_file.pdf')))
            cache['filetype'] = 'pdf'
            print('upload file function - pdf ')
    except:
        result = 'error'

    return result

def process_file():
    doc = None
    if cache['filetype'] == 'tei':
        doc = DocumentHelper.GetDocumentFromTEI()
    else:
        path = ConfigHelper.GetValue("UploadsFolder") + 'input_file.pdf'
        #call text extraction pipeline + xml tei file is getting done here. 
        doc = DocumentHelper.GetDocument(path)
    #time stamp for generating xml file 
   
    #print(" in process_file function - doc")
    #print(doc)
    #store in cache extracted sentences
    sentences = []
    for block in doc.blocks:
        for paragraph in block.paragraphs:
            for sentence in paragraph:
                sentences.append(sentence)
    cache['sentences'] = sentences
                
    #call summarization pipeline
    summ = QSummarization(doc)
    qdoc = summ.SummarizeDocument()

    #store in cache concepts at document level
    cache['phrases'] = qdoc.concepts
    print(qdoc)
    return qdoc

#endregion


#region PDF files

#uploads PDF file
@app.route('/api/', methods = ['POST'])
def upload_pdf_file():
    if request.method == 'POST':
        result = upload_file(request.files['file'])
        return result

#processes PDF file previously uploaded
@app.route('/api/process', methods=["GET"])
def get_by_pdf():
    # comment for the test 
    qdoc = process_file()
    return qdoc.to_json()

#endregion

#uploads TEI/XML file
@app.route('/api/tei', methods = ['POST'])
def upload_tei_file():
    
    if request.method == 'POST':
        result = upload_file(request.files['file'])
        print("/api/tei")
        #print(result)
        return result

#processes TEI/XML file previously uploaded
@app.route('/api/processtei', methods=["GET"])
def get_by_tei():
    qdoc = process_file()
    return qdoc.to_json()

#endregion

#gets clusters of phrases a document level
@app.route('/api/cluster', methods=["POST"])
def get_cluster():
    sentences = cache['sentences']
    phrases = cache['phrases']
    result = clustering.BuildClusters(sentences, phrases)
    print("/api/cluster")
    #print(json.dumps(result))
    return json.dumps(result)

@app.route('/api/sentences', methods=["POST"])
def get_sentences():
    result = request.args.to_dict(flat=False)
    p = request.form['phrase']
    sentences = cache['sentences']
    result = clustering.GetSentences(p, sentences)
   
    return json.dumps(result)

#returns phrases at document level
@app.route('/api/phrases', methods=["GET"])
def get_phrases():
    phrases = cache['phrases']
    return json.dumps(phrases)

#returns TEI/XML file
@app.route('/api/tei', methods=["GET"])
def get_tei():
    with open('./test_files/test.tei.xml', 'r', encoding="utf8") as tei:
            print("tei read new")
            return tei.read()

    print("tei url starts", datetime.now())
    temp_folder = ConfigHelper.GetValue("DumpFolder")
    for (dirpath, dirnames, filenames) in os.walk(temp_folder):
            for filename in filenames:
                if filename.endswith('.tei.xml'):
                    with open(os.sep.join([dirpath, filename]), 'r', encoding="utf8" ) as tei:
                        print("tei read ")
                        #print(tei.read())
                        return tei.read()

#region Methods for accesing configuration file

@app.route('/api/config', methods=["GET"])
def get_config():
    result = ConfigHelper.GetConfigValues()
    return json.dumps(result)

@app.route('/api/config', methods=["POST"])
def set_config():
    params = request.args.to_dict(flat=False)
    p = request.json
    ConfigHelper.SetConfigValues(p)
    ConfigHelper.ReloadFile()
    return "Ok"

#endregion

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000)