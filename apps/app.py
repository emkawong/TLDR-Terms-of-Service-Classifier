import pandas as pd
import numpy as np
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from tosclassifier import ToS_DataCleaner
from tosclassifier import ToS_Classifier

from flask import Flask, render_template, request, jsonify
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/', methods=['GET'])
def index():
    return render_template('classifier.html')

@app.route('/generator.html', methods=['GET'])
def generator():
    return render_template('generator.html')

@app.route('/solve_gen', methods=['POST'])
def solve_gen():
    user_data = request.json
    term = user_data['term_gen']
    model = pickle.load(open('classifier.pkl','rb'))
    X,_ = model.get_data()
    probability = model.predict(X,input_user=True,input_X=term)
    generation = model.get_colors(probability[:,1])[::-1]

    return jsonify({'generation':generation})

@app.route('/solve', methods=['POST'])
def solve():
    user_data = request.json
    term = user_data['term']
    model = pickle.load(open('classifier.pkl','rb'))
    X,_ = model.get_data()
    probability = model.predict(X,input_user=True,input_X=term)
    classification = model.get_colors(probability[:,1])[::-1]

    results = [
        [{'x': 0, 'y': 0}, '#F2DE97'],
        [{'x': 0, 'y': 1}, '#DFEEB9'],
        [{'x': 0, 'y': 2}, '#DFEEB9'],
        [{'x': 0, 'y': 3}, '#FAA181'],
        [{'x': 0, 'y': 4}, '#FAA181'],
        [{'x': 0, 'y': 5}, '#F2DE97'],
        [{'x': 0, 'y': 6}, '#FAA181'],
        [{'x': 0, 'y': 7}, '#FAA181'],
        [{'x': 0, 'y': 8}, '#F77B7E'],
        [{'x': 0, 'y': 9}, '#F77B7E'],
        [{'x': 1, 'y': 0}, '#F77B7E'],
        [{'x': 1, 'y': 1}, '#FAA181'],
        [{'x': 1, 'y': 2}, '#FAA181'],
        [{'x': 1, 'y': 3}, '#FAA181'],
        [{'x': 1, 'y': 4}, '#DFEEB9'],
        [{'x': 1, 'y': 5}, '#DFEEB9'],
        [{'x': 1, 'y': 6}, '#F2DE97'],
        [{'x': 1, 'y': 7}, '#DFEEB9'],
        [{'x': 1, 'y': 8}, '#FAA181'],
        [{'x': 1, 'y': 9}, '#F2DE97'],
        [{'x': 1, 'y': 10}, '#F77B7E'],
        [{'x': 1, 'y': 11}, '#F2DE97'],
        [{'x': 1, 'y': 12}, '#C7FEDD'],
        [{'x': 1, 'y': 13}, '#F2DE97'],
        [{'x': 1, 'y': 14}, '#FAA181'],
        [{'x': 1, 'y': 15}, '#F77B7E'],
        [{'x': 1, 'y': 16}, '#DFEEB9'],
        [{'x': 1, 'y': 17}, '#DFEEB9'],
        [{'x': 1, 'y': 18}, '#FAA181'],
        [{'x': 1, 'y': 19}, '#FAA181'],
        [{'x': 1, 'y': 20}, '#FAA181'],
        [{'x': 2, 'y': 0}, '#C7FEDD'],
        [{'x': 2, 'y': 1}, '#C7FEDD'],
        [{'x': 2, 'y': 2}, '#F2DE97'],
        [{'x': 2, 'y': 3}, '#C7FEDD'],
        [{'x': 2, 'y': 4}, '#FAA181'],
        [{'x': 2, 'y': 5}, '#FAA181'],
        [{'x': 2, 'y': 6}, '#F77B7E'],
        [{'x': 2, 'y': 7}, '#F2DE97'],
        [{'x': 2, 'y': 8}, '#C7FEDD'],
        [{'x': 3, 'y': 0}, '#F2DE97'],
        [{'x': 3, 'y': 1}, '#F2DE97'],
        [{'x': 3, 'y': 2}, '#F2DE97'],
        [{'x': 3, 'y': 3}, '#FAA181'],
        [{'x': 3, 'y': 4}, '#F2DE97'],
        [{'x': 3, 'y': 5}, '#FAA181'],
        [{'x': 3, 'y': 6}, '#F2DE97'],
        [{'x': 3, 'y': 7}, '#F2DE97'],
        [{'x': 3, 'y': 8}, '#F2DE97'],
        [{'x': 3, 'y': 9}, '#DFEEB9'],
        [{'x': 4, 'y': 0}, '#F77B7E'],
        [{'x': 4, 'y': 1}, '#F77B7E'],
        [{'x': 4, 'y': 2}, '#F77B7E'],
        [{'x': 4, 'y': 3}, '#DFEEB9'],
        [{'x': 4, 'y': 4}, '#C7FEDD'],
        [{'x': 4, 'y': 5}, '#F2DE97']]

    for i,color in enumerate(classification):
        results.append([{"x": 5, "y": i},color])

    return jsonify({'results':results})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)