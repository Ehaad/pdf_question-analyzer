from flask import Flask, request, render_template
import PyPDF2
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import itertools

app = Flask(__name__)

def extract_text_from_pdf(file_stream):
    pdf_reader = PyPDF2.PdfReader(file_stream)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def extract_questions(text):
    # Tokenize text into sentences
    sentences = nltk.sent_tokenize(text)
    # Filter out questions
    questions = [sentence for sentence in sentences if sentence.endswith('?')]
    return questions

def find_similar_questions(questions, similarity_threshold=0.5):
    # Vectorize questions
    vectorizer = CountVectorizer().fit_transform(questions)
    vectors = vectorizer.toarray()

    # Compute cosine similarity matrix
    cosine_matrix = cosine_similarity(vectors)

    # Dictionary to store lists of similar questions
    similar_questions_dict = {}

    # Find all questions with similarity above the threshold
    for i, j in itertools.combinations(range(len(questions)), 2):
        if cosine_matrix[i][j] > similarity_threshold:
            if questions[i] not in similar_questions_dict:
                similar_questions_dict[questions[i]] = []
            if questions[j] not in similar_questions_dict:
                similar_questions_dict[questions[j]] = []
            similar_questions_dict[questions[i]].append(questions[j])
            similar_questions_dict[questions[j]].append(questions[i])

    # Flatten the dictionary into a list of unique questions
    similar_questions = []
    for key, similar_list in similar_questions_dict.items():
        similar_questions.extend([key] + similar_list)

    # Remove duplicates by converting to a set and back to a list
    similar_questions = list(set(similar_questions))
    return similar_questions

@app.route('/')
def index():
    return '''
        <html>
        <head>
            <link rel="stylesheet" type="text/css" href="static/styles.css">
        </head>
        <body>
            <h1>Upload PDFs to find similar questions</h1>
            <form action="/upload" method="post" enctype="multipart/form-data">
                <input type="file" name="files" multiple>
                <input type="submit" value="Upload">
            </form>
        </body>
        </html>
    '''

@app.route('/upload', methods=['POST'])
def upload_pdf():
    if 'files' not in request.files:
        return 'No file part', 400

    files = request.files.getlist('files')
    all_questions = []

    for file in files:
        if file and file.filename.endswith('.pdf'):
            text = extract_text_from_pdf(file)
            questions = extract_questions(text)
            all_questions.extend(questions)

    similar_questions = find_similar_questions(all_questions)
    return render_template('result.html', questions=similar_questions)

if __name__ == '__main__':
    app.run(debug=True)
