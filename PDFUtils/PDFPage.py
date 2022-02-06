class PDFPage:

    text = None
    page = None
    method = None
    accuracy = None

    def __init__(self, t, p, m, a = 0):
        self.text = t
        self.page = p
        self.method = m
        self.accuracy = a