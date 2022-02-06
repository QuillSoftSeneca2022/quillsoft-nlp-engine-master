from DataExtraction.DocumentHelper import DocumentHelper
import unittest

class TestGrodibExtraction(unittest.TestCase):
    def test_12papers_2(self):
        '''
        Test blocks and headings extraction
        '''
        data1 = 16
        data2 = []
        data2.append("Introduction")
        data2.append("Materials and methods")
        data2.append("Antiviral compounds")
        data2.append("Viruses")
        data2.append("Viral neuraminidase inhibition assay")
        data2.append("Animal experiment design")
        data2.append("Statistical analysis of animal studies")
        data2.append("Ethics statement for animal studies")
        data2.append("Results")
        data2.append("Viral cytopathic effect inhibition studies")
        data2.append("Viral neuraminidase inhibition experiments")
        data2.append("Efficacy of neuraminidase inhibitors in infected mice")
        data2.append("Efficacy of M2 channel inhibitors in infected mice")
        data2.append("Efficacy of ribavirin in infected mice")
        data2.append("Efficacy of oseltamivir and ribavirin against influenza A/HK-H275Y virus infection in mice")
        data2.append("Discussion")
        set1 = set(data2)

        path = r'./test_files/12papers/2.pdf'
        doc = DocumentHelper.GetDocument(path)
        result1 = len(doc.blocks)
        result2 = []
        result3 = 0
        result4 = 14700

        result3 += len(doc.title)
        result3 += len(doc.abstract)
        for block in doc.blocks:
            result2.append(block.title)
            result3 += len(block.title)
            for p in block.paragraphs:
                for ip in p:                #inner paragraph
                    result3 += len(ip)
        set2 = set(result2)
            
        self.assertGreaterEqual(result1, data1, "Count of blocks is smaller than expected")
        self.assertTrue(set1.issubset(set2), "Headers extracted are not the expected for 12papers 2.")
        self.assertGreaterEqual(result3, result4, "Count of chars is smaller than expected")

    def test_12papers_3(self):
        '''
        Test blocks and headings extraction
        '''
        data1 = 6
        data2 = []
        data2.append("INTRODUCTION")
        data2.append("I. MORPHOLOGY, TYPES & LIFE CYCLE")
        data2.append("RISK FACTORS")
        data2.append("PREVENTION")
        data2.append("TREATMENT")
        data2.append("PROGNOSIS")
        set1 = set(data2)

        path = r'./test_files/12papers/3.pdf'
        doc = DocumentHelper.GetDocument(path)

        result1 = len(doc.blocks)
        result2 = []
        result3 = 0
        result4 = 11900

        result3 += len(doc.title)
        result3 += len(doc.abstract)
        for block in doc.blocks:
            result2.append(block.title)
            result3 += len(block.title)
            for p in block.paragraphs:
                for ip in p:                #inner paragraph
                    result3 += len(ip)
        set2 = set(result2)

        self.assertGreaterEqual(result1, data1, "Count of blocks is smaller than expected")
        self.assertTrue(set1.issubset(set2), "Headers extracted are not the expected for 12papers 3.")
        self.assertGreaterEqual(result3, result4, "Count of chars is smaller than expected")

    def test_12papers_8(self):
        '''
        Test blocks and headings extraction
        '''
        data1 = 6
        data2 = []
        data2.append("INTRODUCTION")
        data2.append("Ebola virus disease")
        data2.append("Middle East respiratory syndrome coronavirus infection")
        data2.append("Swine influenza/ flu")
        data2.append("Zika virus disease")
        data2.append("Conclusions")
        set1 = set(data2)

        path = r'./test_files/12papers/8.pdf'
        doc = DocumentHelper.GetDocument(path)

        result1 = len(doc.blocks)
        result2 = []
        result3 = 0
        result4 = 6000

        result3 += len(doc.title)
        result3 += len(doc.abstract)
        for block in doc.blocks:
            result2.append(block.title)
            result3 += len(block.title)
            for p in block.paragraphs:
                for ip in p:                #inner paragraph
                    result3 += len(ip)
        set2 = set(result2)

        self.assertGreaterEqual(result1, data1, "Count of blocks is smaller than expected")
        self.assertTrue(set1.issubset(set2), "Headers extracted are not the expected for 12papers 8.")
        self.assertGreaterEqual(result3, result4, "Count of chars is smaller than expected")

    def test_28papers_1(self):
        '''
        Test blocks and headings extraction
        '''
        data1 = 16
        data2 = []
        data2.append("INTRODUCTION")
        data2.append("EBOLA EPIDEMIOLOGY Surveillance and Bio-monitoring")
        data2.append("Etiology and Pathophysiology")
        data2.append("TRANSMISSION")
        data2.append("PREVENTION AND CONTROL")
        data2.append("HISTORY")
        data2.append("RECENT OUTBREAK SITUATION IN WEST AFRICA")
        data2.append("CLINICAL MANIFESTATIONS")
        data2.append("System affected Associated signs and symptoms")
        data2.append("SCREENING AND DIAGNOSIS")
        data2.append("Primary Screening")
        data2.append("Secondary Screening")
        data2.append("Entry Screening")
        data2.append("Diagnosis")
        data2.append("TREATMENT AND CLINICAL TRIALS")
        data2.append("CONCLUSION")
        set1 = set(data2)

        path = r'./test_files/28papers/1.pdf'
        doc = DocumentHelper.GetDocument(path)

        result1 = len(doc.blocks)
        result2 = []
        result3 = 0
        result4 = 41000

        result3 += len(doc.title)
        result3 += len(doc.abstract)
        for block in doc.blocks:
            result2.append(block.title)
            result3 += len(block.title)
            for p in block.paragraphs:
                for ip in p:                #inner paragraph
                    result3 += len(ip)
        set2 = set(result2)

        self.assertGreaterEqual(result1, data1, "Count of blocks is smaller than expected")
        self.assertTrue(set1.issubset(set2), "Headers extracted are not the expected for 12papers 8.")
        self.assertGreaterEqual(result3, result4, "Count of chars is smaller than expected")

    def test_12papers_24(self):
        '''
        Test blocks and headings extraction
        '''
        data1 = 4
        data2 = []
        data2.append("INTRODUCTION")
        data2.append("METHODS")
        data2.append("RESULTS")
        data2.append("DISCUSSION")
        set1 = set(data2)

        path = r'./test_files/28papers/24.pdf'
        doc = DocumentHelper.GetDocument(path)

        result1 = len(doc.blocks)
        result2 = []
        result3 = 0
        result4 = 15000

        result3 += len(doc.title)
        result3 += len(doc.abstract)
        for block in doc.blocks:
            result2.append(block.title)
            result3 += len(block.title)
            for p in block.paragraphs:
                for ip in p:                #inner paragraph
                    result3 += len(ip)
        set2 = set(result2)

        self.assertGreaterEqual(result1, data1, "Count of blocks is smaller than expected")
        self.assertTrue(set1.issubset(set2), "Headers extracted are not the expected for 12papers 8.")
        self.assertGreaterEqual(result3, result4, "Count of chars is smaller than expected")

if __name__ == '__main__':
    unittest.main()