from collections import Counter
import PyPDF2
import textract

from flask import Flask, jsonify, request
from flask_cors import CORS
app = Flask(__name__)

from distutils import extension
import os
import docx
from cmath import nan
import pandas as pd
CORS(app)



@app.route('/count', methods=['POST'])
def upload():
    
    if request.method == 'POST':
        f = request.files['file']
        str_file = str(f.filename)

        split_tuple = os.path.splitext(str_file)
        file_extension = split_tuple[1]

        print(f)
        def parsePdf(f):
            pdfReader = PyPDF2.PdfFileReader(f)

            num_pages = pdfReader.numPages
            count = 0
            text = ""

            while count < num_pages:
                pageObj = pdfReader.getPage(count)
                count += 1
                text += pageObj.extractText()

            if text != "":
                text = text

            else:
                text = textract.process('', method='tesseract', language='eng')

            text_from_PDF = ''.join(text).split()
            return text_from_PDF

        def parseWord(f):
            
            doc = docx.Document(f)
            result = []
            for p in doc.paragraphs:
                curr = p.text
                res = curr.split()
                result += res
            return result

        def parseExcel(f):
            workbook = pd.read_excel(f, None)
            sheets = workbook.keys()
            all_words = []

            for key in sheets:
                curr_sheet = workbook[key]
                for data in curr_sheet:
                    for item in curr_sheet[data]:
                        if str(item) == 'nan':
                            continue
                        all_words.append(str(item))
            return all_words
        parsed = None
        if file_extension == ".pdf":
            parsed = parsePdf(f)
        if file_extension == ".docx":
            parsed = parseWord(f)
        if file_extension == ".xlsx":
            parsed = parseExcel(f)
        

        result = count_words(parsed)
        print(result,"line 81")
        return jsonify(unique_words=result[0], total_words=result[1])


# counter for a pdf file
def count_words(words):
    words = [each_word.lower() for each_word in words]
    count = Counter(words)
    unique_words = 0

    for word in count:
        if count[word] == 1:
            unique_words += 1

    return unique_words, len(words)


if __name__ == "__main__":
    app.run()
