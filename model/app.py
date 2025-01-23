from flask import Flask, request, jsonify
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import os

app = Flask(__name__)

# Load pre-saved model components
MODEL_PATH = "machine_downtime_model.pkl"
IMPUTER_PATH = "imputer.pkl"
TRANSFORMER_PATH = "transformer.pkl"
ENCODER_PATH = "encoder.pkl"
COLUMNS_PATH = "columns.pkl"

if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
else:
    model = None

if os.path.exists(IMPUTER_PATH):
    imputer = joblib.load(IMPUTER_PATH)
else:
    imputer = None

if os.path.exists(TRANSFORMER_PATH):
    transformer = joblib.load(TRANSFORMER_PATH)
else:
    transformer = None

if os.path.exists(ENCODER_PATH):
    encoder = joblib.load(ENCODER_PATH)
else:
    encoder = None

if os.path.exists(COLUMNS_PATH):
    feature_columns = joblib.load(COLUMNS_PATH)
else:
    feature_columns = None


@app.route('/upload', methods=['POST'])
def upload_data():
    """Upload a CSV file containing manufacturing data."""
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    try:
        df = pd.read_csv(file)
        df.to_csv("uploaded_data.csv", index=False)
        return jsonify({"message": "File uploaded successfully", "data_preview": df.head().to_dict()}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to process file: {str(e)}"}), 500


@app.route('/train', methods=['POST'])
def train_model():
    """Validate the uploaded dataset and evaluate the saved model's performance."""
    global model, imputer, transformer, encoder, feature_columns

    # Ensure all required components are loaded
    if not all([model, imputer, transformer, encoder, feature_columns]):
        return jsonify({"error": "Pretrained model and components are not properly loaded. Ensure all required files are present."}), 400

    # Load the uploaded dataset
    try:
        df = pd.read_csv("uploaded_data.csv")
    except FileNotFoundError:
        return jsonify({"error": "No uploaded dataset found. Please upload data first."}), 400

    # Define the target column
    target = "Downtime"
    if target not in df.columns:
        return jsonify({"error": f"Target column '{target}' not found in uploaded data."}), 400

    # Validate feature columns
    missing_features = [col for col in feature_columns if col not in df.columns]
    if missing_features:
        return jsonify({"error": f"Uploaded data is missing required feature columns: {missing_features}"}), 400

    # Preprocess the data
    try:
        # Transform target using encoder
        df[target] = encoder.transform(df[target])

        X = df[feature_columns]
        y = df[target]

        # Apply preprocessing
        X = imputer.transform(X)
        X = transformer.transform(X)

        # Evaluate model performance
        y_pred = model.predict(X)
        accuracy = accuracy_score(y, y_pred)
        report = classification_report(y, y_pred, output_dict=True)

        return jsonify({
            "message": "Model evaluation completed successfully",
            "accuracy": accuracy,
            "classification_report": report
        }), 200
    except Exception as e:
        return jsonify({"error": f"Failed to process dataset or evaluate model: {str(e)}"}), 500


@app.route('/predict', methods=['POST'])
def predict_downtime():
    """Accept JSON input and return the prediction with confidence."""
    data = request.get_json()

    if not data:
        return jsonify({"error": "No input data provided"}), 400

    # Ensure all required features are provided
    if not feature_columns:
        return jsonify({"error": "Feature columns not defined in saved model."}), 400

    try:
        # Create a DataFrame from input
        input_df = pd.DataFrame([data])
        input_df = input_df.reindex(columns=feature_columns, fill_value=0)

        # Apply preprocessing
        if imputer:
            input_df = pd.DataFrame(imputer.transform(input_df), columns=feature_columns)

        if transformer:
            input_df = pd.DataFrame(transformer.transform(input_df), columns=feature_columns)

        # Make predictions
        prediction_encoded = model.predict(input_df)[0]
        probabilities = model.predict_proba(input_df)[0]  # Get probabilities for all classes

        prediction = encoder.inverse_transform([prediction_encoded])[0]
        confidence = max(probabilities)  # Confidence is the probability of the predicted class

        return jsonify({"prediction": prediction, "confidence": confidence}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to make prediction: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
