from flask import Flask, request, jsonify, render_template, redirect, url_for
import numpy as np
import pandas as pd
import pickle
import joblib
import os
import tensorflow as tf
import warnings
warnings.filterwarnings('ignore')
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Define global variables for models
scaler = None
column_names = None
decision_tree = None
neural_network = None
svm = None
cnn_model = None

def load_models():
    global scaler, column_names, decision_tree, neural_network, svm, cnn_model
    print("Loading models...")
    scaler = joblib.load('models/scaler.pkl')
    with open('models/column_names.pkl', 'rb') as f:
        column_names = pickle.load(f)
    decision_tree = joblib.load('models/decision_tree_model.pkl')
    neural_network = joblib.load('models/neural_network_model.pkl')
    svm = joblib.load('models/svm_model.pkl')
    cnn_model = tf.keras.models.load_model('models/cnn_model')
    print("✓ All models loaded successfully!")

@app.before_request
def before_request():
    global scaler
    if scaler is None:
        load_models()

def preprocess_input(data):
    input_df = pd.DataFrame([data])
    missing_cols = set(column_names) - set(input_df.columns)
    if missing_cols:
        return None, f"Missing required features: {', '.join(missing_cols)}"
    input_df = input_df[column_names]
    input_array = input_df.values
    input_scaled = scaler.transform(input_array)
    input_cnn = np.array(input_scaled).reshape(input_scaled.shape[0], input_scaled.shape[1], 1)
    return {
        'raw': input_array,
        'scaled': input_scaled,
        'cnn': input_cnn
    }, None

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/predict_ui', methods=['POST'])
def predict_ui():
    try:
        data = {
            'age': int(request.form['age']),
            'sex': int(request.form['sex']),
            'cp': int(request.form['cp']),
            'trestbps': int(request.form['trestbps']),
            'chol': int(request.form['chol']),
            'fbs': int(request.form['fbs']),
            'restecg': int(request.form['restecg']),
            'thalach': int(request.form['thalach']),
            'exang': int(request.form['exang']),
            'oldpeak': float(request.form['oldpeak']),
            'slope': int(request.form['slope']),
            'ca': int(request.form['ca']),
            'thal': int(request.form['thal']),
        }
        inputs, error = preprocess_input(data)
        if error:
            return render_template('error.html', error=error)
        dt_pred = int(decision_tree.predict(inputs['raw'])[0])
        nn_pred = int(neural_network.predict(inputs['scaled'])[0])
        svm_pred = int(svm.predict(inputs['scaled'])[0])
        cnn_pred = int((cnn_model.predict(inputs['cnn']) > 0.5)[0][0])
        predictions = [dt_pred, nn_pred, svm_pred, cnn_pred]
        ensemble_pred = int(np.bincount(predictions).argmax())
        nn_prob = float(neural_network.predict_proba(inputs['scaled'])[0][1])
        svm_prob = float(svm.predict_proba(inputs['scaled'])[0][1])
        cnn_prob = float(cnn_model.predict(inputs['cnn'])[0][0])
        results = {
            'decision_tree': {
                'class': dt_pred,
                'probability': None,
                'label': 'Heart Disease' if dt_pred == 0 else 'No Heart Disease'
            },
            'neural_network': {
                'class': nn_pred,
                'probability': round((1 - nn_prob) * 100, 2) if nn_pred == 0 else round(nn_prob * 100, 2),
                'label': 'Heart Disease' if nn_pred == 0 else 'No Heart Disease'
            },
            'svm': {
                'class': svm_pred,
                'probability': round((1 - svm_prob) * 100, 2) if svm_pred == 0 else round(svm_prob * 100, 2),
                'label': 'Heart Disease' if svm_pred == 0 else 'No Heart Disease'
            },
            'cnn': {
                'class': cnn_pred,
                'probability': round((1 - cnn_prob) * 100, 2) if cnn_pred == 0 else round(cnn_prob * 100, 2),
                'label': 'Heart Disease' if cnn_pred == 0 else 'No Heart Disease'
            },
            'ensemble': {
                'class': ensemble_pred,
                'label': 'Heart Disease' if ensemble_pred == 0 else 'No Heart Disease'
            }
        }
        positive_count = sum([1 for model, result in results.items() if model != 'ensemble' and result['class'] == 0])
        return render_template('result.html', results=results, data=data, positive_count=positive_count, total_models=4)
    except Exception as e:
        return render_template('error.html', error=str(e))

@app.route('/api/predict', methods=['POST'])
def predict_api():
    try:
        data = request.json
        inputs, error = preprocess_input(data)
        if error:
            return jsonify({'error': error}), 400
        dt_pred = int(decision_tree.predict(inputs['raw'])[0])
        nn_pred = int(neural_network.predict(inputs['scaled'])[0])
        svm_pred = int(svm.predict(inputs['scaled'])[0])
        cnn_pred = int((cnn_model.predict(inputs['cnn']) > 0.5)[0][0])
        predictions = [dt_pred, nn_pred, svm_pred, cnn_pred]
        ensemble_pred = int(np.bincount(predictions).argmax())
        nn_prob = float(neural_network.predict_proba(inputs['scaled'])[0][1])
        svm_prob = float(svm.predict_proba(inputs['scaled'])[0][1])
        cnn_prob = float(cnn_model.predict(inputs['cnn'])[0][0])
        return jsonify({
            'predictions': {
                'decision_tree': {
                    'class': dt_pred,
                    'label': 'Heart Disease' if dt_pred == 0 else 'No Heart Disease'
                },
                'neural_network': {
                    'class': nn_pred,
                    'probability': (1 - nn_prob) if nn_pred == 0 else nn_prob,
                    'label': 'Heart Disease' if nn_pred == 0 else 'No Heart Disease'
                },
                'svm': {
                    'class': svm_pred,
                    'probability': (1 - svm_prob) if svm_pred == 0 else svm_prob,
                    'label': 'Heart Disease' if svm_pred == 0 else 'No Heart Disease'
                },
                'cnn': {
                    'class': cnn_pred,
                    'probability': (1 - cnn_prob) if cnn_pred == 0 else cnn_prob,
                    'label': 'Heart Disease' if cnn_pred == 0 else 'No Heart Disease'
                },
                'ensemble': {
                    'class': ensemble_pred,
                    'label': 'Heart Disease' if ensemble_pred == 0 else 'No Heart Disease'
                }
            },
            'input_data': data
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/presets', methods=['GET'])
def presets():
    return render_template('presets.html')

if __name__ == '__main__':
    os.makedirs('templates', exist_ok=True)
    print("Initializing models at startup...")
    load_models()
    app.run(debug=False, host='0.0.0.0', port=5000) 