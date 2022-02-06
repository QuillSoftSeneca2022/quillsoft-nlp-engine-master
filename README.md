# quillsoft-nlp-engine

Most of the libraries listed under Required Libraries can be installed using the command `pip install -r requirements.txt`
Exceptions include GROBID, SPACY language packages and Flask-CORS

It is necessary to install manually the libraries in which its description is detailed the version number (e.g. spacy, gensim, textacy...)

```
pip install --upgrade <<library name>>==<<version>>
```

# Required Libraries

## PyMuPDF

Version 1.18.8
- pip install PyMuPDF

## PDFKit

- pip install pdfkit

```
Linux:
- sudo apt-get install wkhtmltopdf
Windows:
- https://wkhtmltopdf.org/downloads.html

- Set the key "PDFKitExecutablePath" in the config.json file
```

## BeautifulSoup

- pip install BeautifulSoup4

## num2words

- pip install num2words

## Contractions

Version 0.0.48
- pip install contractions

## Requests

- pip install requests

## Dataclasses-JSON

- pip install dataclasses-json

## lxml

- pip install lxml

## GROBID

- Requires JVM 10 or lower (not compatible with JVM 11)
- https://grobid.readthedocs.io/en/latest/

```
- wget https://github.com/kermitt2/grobid/archive/0.6.1.zip
- unzip 0.6.1.zip
- ./gradlew clean install
- ./gradlew run
```

## SPACY

Version 3.0.3
```
- pip install spacy
- python -m spacy download en_core_web_sm
- python -m spacy download en_core_web_md
- python -m spacy download en_core_web_lg
```

## TEXTACY

Version 0.10.0
```
- pip install textacy

Optional
Will always use the english library:
- python -m spacy link en_core_web_md en
```

## PyTextRank

```
- pip install pytextrank
```

## Gensim

Version 3.8.3
```
- pip install gensim
```

## Scikit-Learn

```
- pip install sklearn
```

## Flask

```
- pip install flask
- also requires flask-cors which can be installed with pip install -U flask-cors

Start flask server:
- python -m flask run
```

## NumPy

```
- pip install numpy
```

# Configuration

## Text extraction

- **ElementsToRemove**: Lists of regular expressions of elements to remove in the text of the pdf. e.g. text within parentheses.
- **SectionsToRemove**: Lists of regular expressions of sections to remove if it contains the given sequence of characters. e.g. description of figures or tables..
- **BlackListWords**: Lists of words to be removed from the text including the section (upper case). e.g. "Corresponding author. Tel.: +1 435 797 2897; fax: +1 435 797 3959 #####"
- **WhiteListHeadings**: Lists of words to be maintained and formatted properly to be recognized as a valid heading. e.g. A B S T R A C T.
- **MinAlphaInBlock**: Minimum of the percentage of alpha characters in a section allowed. e.g. if less than 50% of the chars in a section are letters, probably these sections belong to a table with several numbers or symbols.
- **CustomTranslations**: List of symbols or words to be arbitrarily replaced with new text. e.g. % to percent
- **CustomContractions**: List of additional tuples to be added to the contractions library of python.

# General

- **grobid_server**: Grobid server URL,
- **grobid_port**: Grobid Server Port,
- **DumpFolder**: Path of a folder to store temporary files produced by the execution of the app.
- **PDFKitExecutablePath**: Path of the executable of wkhtmltopdf application.
```
- Windows: C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe
- Linux: /usr/bin/wkhtmltopdf
```

# How to run Text Extraction Pipeline

## With GROBID Service (online)

Be sure the GROBID service is online and the endpoint in the configuration file is properly set.

```
from DataExtraction.DocumentHelper import DocumentHelper
path = r'./test_files/28papers/1.pdf'
doc = DocumentHelper.GetDocument(path)
```

"doc" variable will hold a DataClasses.Document object Type which can be iterated by blocks and then by paragraphs to get the text of the articles.

## Without GROBID Service (offline)

The application will load up pre-processed JSON files (12papers and 28papers files).

```
from Helpers.TestHelper import GetText
doc = GetText("12papers", 2)
```

"doc" variable will hold a DataClasses.Document object which can be iterated by blocks and then by paragraphs to get the text of the articles.

# How to run Summarization Pipeline

(offline)

```
from Helpers.TestHelper import GetText
from Summarization.QSummarization import QSummarization
#Call Text Extraction pipeline
doc = GetText("28papers", 24)
#Call Summarization pipeline
summ = QSummarization(doc)
qdoc = summ.SummarizeDocument()
```

"qdoc" variable will hold a DataClasses.QDocument object which can be iterated by Sections, Paragraphs, and Keywords.


## Flask API Service

- SummarizationController.py

```
python .\Controllers\SummarizationController.py
```

## Update Libraries

```
pip install PyMuPDF --upgrade
pip install contractions --upgrade
pip install spacy --upgrade
pip install pytextrank --upgrade
pip install PyMuPDF --upgrade
```
- Spacy requires to reinstall latest version of models
```
python -m spacy download en_core_web_sm
python -m spacy download en_core_web_md
python -m spacy download en_core_web_lg
```

## Train Word2Vec Model

```
python .\TrainWord2VecModel.py
```
It will generate three files inside the Directory "Models". These files are necessary for the clusterization feature.
