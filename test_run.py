from Helpers.TestHelper import GetText
from Summarization.QSummarization import QSummarization
#Call Text Extraction pipeline
doc = GetText("28papers", 24)
#Call Summarization pipeline
summ = QSummarization(doc)
qdoc = summ.SummarizeDocument()