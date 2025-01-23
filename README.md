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
    
# Instructions for Testing with Postman

## Set Up Postman  
1. Open Postman and create a new request.  
2. Select the appropriate HTTP method (e.g., `POST`).  
3. Enter the API endpoint URL (e.g., `http://127.0.0.1:5000/<endpoint>`).  

---

## Testing Each Endpoint  

### Upload Endpoint  
- **HTTP Method:** `POST`  
- **URL:** `http://127.0.0.1:5000/upload`  
- **Body Type:** `form-data`  
  - Add a key named `file` and select the CSV file to upload.  
- **Example Response:**  
  ```json
  {
    "data_preview": {
        "Air_System_Pressure(bar)": {
            "0": 6.284964506,
            "1": 6.19673253,
            "2": 6.655448451,
            "3": 6.560393963,
            "4": 6.141237748
        },
        "Assembly_Line_No": {
            "0": "Shopfloor-L1",
            "1": "Shopfloor-L1",
            "2": "Shopfloor-L3",
            "3": "Shopfloor-L2",
            "4": "Shopfloor-L1"
        },
        "Coolant_Pressure(bar)": {
            "0": 6.933724915,
            "1": 4.936891865,
            "2": 6.839413159,
            "3": 4.574382007,
            "4": 6.893181921
        },
        "Coolant_Temperature": {
            "0": 25.6,
            "1": 35.3,
            "2": 13.1,
            "3": 24.4,
            "4": 4.1
        },
        "Cutting(kN)": {
            "0": 3.58,
            "1": 2.68,
            "2": 3.55,
            "3": 3.55,
            "4": 3.55
        },
        "Date": {
            "0": "31-12-2021",
            "1": "31-12-2021",
            "2": "31-12-2021",
            "3": "31-05-2022",
            "4": "31-03-2022"
        },
        "Downtime": {
            "0": "Machine_Failure",
            "1": "Machine_Failure",
            "2": "Machine_Failure",
            "3": "Machine_Failure",
            "4": "Machine_Failure"
        },
        "Hydraulic_Oil_Temperature(?C)": {
            "0": 46.0,
            "1": 47.4,
            "2": 40.7,
            "3": 44.2,
            "4": 47.3
        },
        "Hydraulic_Pressure(bar)": {
            "0": 71.04,
            "1": 125.33,
            "2": 71.12,
            "3": 139.34,
            "4": 60.51
        },
        "Machine_ID": {
            "0": "Makino-L1-Unit1-2013",
            "1": "Makino-L1-Unit1-2013",
            "2": "Makino-L3-Unit1-2015",
            "3": "Makino-L2-Unit1-2015",
            "4": "Makino-L1-Unit1-2013"
        },
        "Spindle_Bearing_Temperature(?C)": {
            "0": 33.4,
            "1": 34.6,
            "2": 33.0,
            "3": 40.6,
            "4": 31.4
        },
        "Spindle_Speed(RPM)": {
            "0": 25892.0,
            "1": 19856.0,
            "2": 19851.0,
            "3": 18461.0,
            "4": 26526.0
        },
        "Spindle_Vibration(?m)": {
            "0": 1.291,
            "1": 1.382,
            "2": 1.319,
            "3": 0.618,
            "4": 0.983
        },
        "Tool_Vibration(?m)": {
            "0": 26.492,
            "1": 25.274,
            "2": 30.608,
            "3": 30.791,
            "4": 25.516
        },
        "Torque(Nm)": {
            "0": 24.05532601,
            "1": 14.20288973,
            "2": 24.04926704,
            "3": 25.86002925,
            "4": 25.51587386
        },
        "Voltage(volts)": {
            "0": 335.0,
            "1": 368.0,
            "2": 325.0,
            "3": 360.0,
            "4": 354.0
        }
    },
    "message": "File uploaded successfully"
}
### Train Endpoint
- **HTTP Method:** `POST`  
- **URL:** `http://127.0.0.1:5000/train`  
- **Body Type:** None

- **Example Response:**  
  ```json
  {
    "accuracy": 0.9976,
    "classification_report": {
        "0": {
            "f1-score": 0.997626582278481,
            "precision": 0.9984164687252574,
            "recall": 0.9968379446640316,
            "support": 1265.0
        },
        "1": {
            "f1-score": 0.9975728155339806,
            "precision": 0.9967663702506063,
            "recall": 0.9983805668016195,
            "support": 1235.0
        },
        "accuracy": 0.9976,
        "macro avg": {
            "f1-score": 0.9975996989062308,
            "precision": 0.9975914194879318,
            "recall": 0.9976092557328256,
            "support": 2500.0
        },
        "weighted avg": {
            "f1-score": 0.9976000215066979,
            "precision": 0.9976013200787798,
            "recall": 0.9976,
            "support": 2500.0
        }
    },
    "message": "Model evaluation completed successfully"
}

### Predict Endpoint
- **HTTP Method:** `POST`  
- **URL:** `http://127.0.0.1:5000/predict`  
- **Body Type:** `raw (JSON format)`  
  - Add a key named `file` and select the CSV file to upload.
- **Example Input: Use the input.json file in the model folder**  
  
- **Example Response:**  
  ```json
  {
    "confidence": 1.0,
    "prediction": "Machine_Failure"
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
