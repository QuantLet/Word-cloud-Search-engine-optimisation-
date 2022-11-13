import os
import re
import time

import PyPDF2
import requests as requests
from nltk.stem import PorterStemmer

from exceptions.PDFDownloadException import PDFDownloadException


class PDFManager:
    def __init__(self, url):
        self.url = url
        self.file_name = self.url.rsplit('/', 1)[-1]
        self.ps = PorterStemmer()

    def clean(self):
        '''PDF cleaning procedure'''

        pdf_output, totalpages = self.get_string()

        # # cleaning URLs
        pdf_output = [re.sub(pattern="http[^ ]*", repl=" ", string=pdf_output[i]) for i in range(totalpages)]

        # # cleaning symbols
        pdf_output = [re.sub(pattern="\\n", repl=" ", string=pdf_output[i]) for i in range(totalpages)]
        pdf_output = [re.sub(pattern="\W|\d", repl=" ", string=pdf_output[i]) for i in range(totalpages)]
        pdf_output = [re.sub(pattern="[^a-zA-Z]", repl=" ", string=pdf_output[i]) for i in range(totalpages)]

        # # cleaning multispaces
        pdf_output = [re.sub(pattern="\s{2,}", repl=" ", string=pdf_output[i]) for i in range(totalpages)]

        # # cleaning out 1-2-worders
        pdf_output = [re.sub(pattern=" .{1,2} ", repl=" ", string=pdf_output[i]) for i in range(totalpages)]
        pdf_output = [re.sub(pattern=" .{1,2} ", repl=" ", string=pdf_output[i]) for i in range(totalpages)]
        pdf_output = [re.sub(pattern=" .{1,2} ", repl=" ", string=pdf_output[i]) for i in range(totalpages)]

        # # lower-casing
        pdf_output = [pdf_output[i].lower() for i in range(totalpages)]
        pdf_output = [[self.ps.stem(word) for word in sentence.split(" ")] for sentence in pdf_output]
        pdf_output = [' '.join(pdf_output[i]) for i in range(len(pdf_output))]

        return pdf_output, totalpages

    def get_string(self):
        '''Transform a PDF file to a list of string pages'''

        try:
            self.download()

            # opening the file
            imported_pdf = open(self.file_name, 'rb')
            # removing the file locally
            os.remove(self.file_name)

            # convert PDF to readable file
            transformed_pdf = PyPDF2.PdfFileReader(imported_pdf, strict=False)

            # get number of pages
            totalpages = transformed_pdf.numPages

            # read the data and store in a list
            pdf_output = [transformed_pdf.getPage(i) for i in range(totalpages)]

            # extract result
            pdf_output = [pdf_output[i].extractText() for i in range(totalpages)]

            return pdf_output, totalpages
        except PDFDownloadException:
            print("Cannot download PDF file.")

    def get_search_data(self):
        '''Creating the final dataframe'''

        t = time.process_time()
        # clean the first pdf
        pdf_output, totalpages = self.clean()

        # combine the pdf
        combined_pdf = [' '.join(pdf_output)]

        try:
            pdf_output, totalpages = self.clean()
            combined_pdf.append(' '.join(pdf_output))
        except:
            print('problematic file, %s', self.url)
            combined_pdf.append(' '.join(''))
        finally:
            duration = time.process_time() - t

        return combined_pdf[0], duration

    def download(self):
        '''Download a PDF file via an URL'''

        # Define HTTP Headers
        headers = {"User-Agent": "Chrome/51.0.2704.103"}

        # Download image
        response = requests.get(self.url, headers=headers)

        # if response is OK download the PDF and store it, else print the status
        if response.status_code == 200:
            with open(self.file_name, "wb") as f:
                f.write(response.content)
            return True
        else:
            raise PDFDownloadException("Could not download PDF File, code: %s", response.status_code)