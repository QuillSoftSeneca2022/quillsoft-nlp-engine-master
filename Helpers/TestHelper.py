from DataClasses.Document import Document
from dataclasses_json import dataclass_json


def GetText(file, article):
    f = open("./test_files/test_input/" + file + str(article) + ".json", "r")
    return Document.from_json(f.read())
