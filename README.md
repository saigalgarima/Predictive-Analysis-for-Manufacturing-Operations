# Predictive-Analysis-for-Manufacturing-Operations
This project provides a RESTful API to predict machine downtime or production defects based on manufacturing data using a Random Forest Classifier. The API includes endpoints for data upload, model training, and prediction with confidence scores.

---

# Endpoints

1. Upload Endpoint
POST /upload
Upload a CSV file with feature columns like Hydraulic_Pressure(bar), Coolant_Pressure(bar), etc.
**Example cURL**:  
   ```bash
   curl -X POST -F "file=@path_to_csv_file.csv" http://127.0.0.1:5000/upload


2. Train Endpoint
  POST /train
  Trains the model and returns accuracy and F1-score.
    ```bash

    Response Example:
      {
        "message": "Model evaluation completed successfully",
        "accuracy": 0.92
      }
  

3. Predict Endpoint
    POST /predict
    Accepts JSON input with feature values and returns a prediction with confidence.
    
    Input Example (JSON):
    For testing purposes, you can use the input.json file in the testing folder.
   ```bash


    Response Example:
    {
      "prediction": "No_Machine_Failure",
      "confidence": 0.87
    }
    
    

# Preloaded Components
- machine_downtime_model.pkl: Trained model.
- imputer.pkl: Handles missing values.
- transformer.pkl: Normalization.
- columns.pkl: Feature columns.
- encoder.pkl: Target label encoder.

---

# Sample Dataset
A sample CSV file, Machine Downtime.csv, is provided in the model folder in the repository.

---

# Setup

1. Clone the Repository
   ```bash
    git clone <repository-url>
    cd <repository-folder>

2. Install Dependencies
   ```bash
   pip install -r requirements.txt

3. Run the App
    ```bash
    python app.py
