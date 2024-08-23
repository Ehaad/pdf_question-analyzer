# PDF Question Analyzer

PDF Question Analyzer is a Flask-based web application that allows users to upload multiple PDFs containing questions. The app extracts all questions from the uploaded PDFs and identifies similar questions based on cosine similarity. This tool is useful for educators, students, or anyone looking to analyze and group similar questions from multiple documents.

## Features

- Upload multiple PDF files at once.
- Extracts questions from the text in PDFs.
- Identifies and displays similar questions based on content.
- Simple web interface for ease of use.

## Technologies Used

- Python
- Flask
- NLTK (Natural Language Toolkit)
- PyPDF2
- Scikit-learn
