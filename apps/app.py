import pandas as pd
import numpy as np
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

from flask import Flask, render_template, request, jsonify
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/', methods=['GET'])
def index():
    return render_template('classifier.html')

@app.route('/solve', methods=['POST'])
def solve():
    user_data = request.json
    term = user_data['term']
    tfidf_model = pickle.load(open('tfidf.sav','rb'))
    loaded_model = pickle.load(open('model.sav', 'rb'))
    input_vectorized = tfidf_model.transform(pd.Series(term)).toarray()
    classification = str(loaded_model.predict(input_vectorized))
    
    # Edit this to return the array of points from the solution computed above
    results = [
        # x: Company / y: Paragraph
        {"x": 1, "y": 1, "color": "red"},
        {"x": 2, "y": 1, "color": "red"},
        {"x": 3, "y": 1, "color": "red"},
        {"x": 4, "y": 1, "color": "red"},
        {"x": 5, "y": 1, "color": "red"},
    ]

    return jsonify({'results':results})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
