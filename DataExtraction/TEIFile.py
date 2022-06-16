from bs4 import BeautifulSoup
from DataClasses.Person import Person

class TEIFile(object):
    def __init__(self, filename):
        self.filename = filename
        self.soup = self.read_ltei()
        self.xsoup = self.read_xtei()
        self._text = None
        self._title = ''
        self._abstract = ''

    @property
    def doi(self):
        idno_elem = self.soup.find('idno', type='DOI')
        if not idno_elem:
            return ''
        else:
            return idno_elem.getText()

    @property
    def title(self):
        if not self._title:
            self._title = self.soup.title.getText()
        return self._title

    @property
    def body(self):
        divs = []

        body = self.xsoup.find_all('body')[0]
        for div in body.find_all('div'):
            divs.append(div)
        return divs

    @property
    def abstract(self):
        if not self._abstract:
            abstract = self.soup.abstract.getText(separator=' ', strip=True)
            self._abstract = abstract
        return self._abstract

    @property
    def authors(self):
        authors_in_header = self.soup.analytic.find_all('author')

        result = []
        for author in authors_in_header:
            persname = author.persname
            if not persname:
                continue
            firstname = self.elem_to_text(persname.find("forename", type="first"))
            middlename = self.elem_to_text(persname.find("forename", type="middle"))
            surname = self.elem_to_text(persname.surname)
            person = Person(firstname, middlename, surname)
            result.append(person)
        return result
    
    @property
    def text(self):
        if not self._text:
            divs_text = []
            for div in self.soup.body.find_all("div"):
                # div is neither an appendix nor references, just plain text.
                if not div.get("type"):
                    div_text = div.get_text(separator=' ', strip=True)
                    divs_text.append(div_text)

            plain_text = " ".join(divs_text)
            self._text = plain_text
        return self._text

    def read_ltei(self):
        with open(self.filename, 'r', encoding="utf8") as tei:
            soup = BeautifulSoup(tei, 'lxml')
            return soup
        raise RuntimeError('Cannot generate a soup from the input')

    def read_xtei(self):
        with open(self.filename, 'r', encoding="utf8") as tei:
            soup = BeautifulSoup(tei, 'xml')
            return soup
        raise RuntimeError('Cannot generate a soup from the input')

    def elem_to_text(self, elem, default=''):
        if elem:
            return elem.getText()
        else:
            return default