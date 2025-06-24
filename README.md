# CNN-for-Heart-Disease-Prediction

A comprehensive heart disease prediction system using a Convolutional Neural Network (CNN) and multiple machine learning models, with a web interface for user-friendly predictions.

## Project Overview

This project leverages the Cleveland Heart Disease dataset to build, train, and compare several machine learning models for heart disease prediction, including:

- Decision Tree
- Neural Network (MLP)
- Support Vector Machine (SVM)
- XGBoost
- A custom Convolutional Neural Network (CNN)

The system features:

- Data preprocessing and exploratory data analysis (EDA)
- Model training and evaluation
- Ensemble prediction
- A Flask-based web application for interactive predictions
- Comparison with published research results

## Dataset

- **Source:** Cleveland Heart Disease dataset
- **File:** `assets/heart.csv`
- The dataset is preprocessed and used for both training and inference.

## Web Application

The project includes a Flask web app (`app.py`) with the following features:

- User-friendly form for inputting patient data
- Real-time predictions from all models and ensemble
- Probability/confidence scores for each model
- Error handling and informative feedback
- Preset examples for quick testing

### Templates

- `templates/index.html`: Main input form
- `templates/result.html`: Displays prediction results
- `templates/error.html`: Error messages
- `templates/presets.html`: Example input presets

## Model Artifacts

Trained models are stored in the `models/` directory:

- `cnn_model/` (TensorFlow SavedModel format)
- `decision_tree_model.pkl`
- `neural_network_model.pkl`
- `svm_model.pkl`
- `xgboost_model.pkl`
- `scaler.pkl`, `column_names.pkl` (for preprocessing)

## Visualizations & Assets

Key visualizations and analysis results are provided in the `assets/` directory:

- Model comparison: `assets/model_comparison.png`
- CNN training history: `assets/cnn_training_history.png`
- SVM ROC curves: `assets/svm_linear_roc.png`, `assets/svm_poly_roc.png`, `assets/svm_rbf_roc.png`, `assets/svm_sigmoid_roc.png`
- XGBoost feature importance: `assets/xgboost_feature_importance.png`
- EDA: `assets/heart_eda.png`, `assets/heart_eda_summary.png`

## Getting Started

### 1. Clone the Repository

```sh
git clone <repo-url>
cd CNN-for-Heart-Disease-prediction
```

### 2. Set Up the Environment (Windows)

Run the provided setup script to ensure Python 3.9.13 and all dependencies are installed:

```sh
setup_env_and_install.bat
```

Alternatively, set up manually:

```sh
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run the Web Application

**Recommended:** Use the provided batch file to activate the environment and start the app:

```sh
run_app.bat
```

Or, you can start the app manually:

```sh
venv\Scripts\activate
python app.py
```

The app will be available at [http://localhost:5000](http://localhost:5000)

## Usage

- Open your browser and go to `http://localhost:5000`
- Fill in the patient data form and submit
- View predictions from all models and the ensemble
- Use the presets page for example inputs

## Notebooks & Research

- The Jupyter notebook `CNNmodel.ipynb` contains all data analysis, model training, and evaluation code.
- The file `assets/heartcnnpaper.docx` provides a research paper-style writeup and comparison with published results.

## References

- Cleveland Heart Disease dataset: [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/heart+Disease)
- TensorFlow, scikit-learn, XGBoost, Flask

## License

This project is for educational and research purposes.
