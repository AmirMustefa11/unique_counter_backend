from collections import Counter
import PyPDF2
import textract

from flask import Flask, jsonify, request
app = Flask(__name__)


@app.route('/count', methods=['POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
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
        result = count_words(text_from_PDF)
        return jsonify(unique_words=result[0], total_words=result[1])


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
