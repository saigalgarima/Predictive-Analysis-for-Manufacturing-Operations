# Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix,f1_score
from sklearn.preprocessing import PowerTransformer, LabelEncoder
from sklearn.impute import SimpleImputer
import seaborn as sns
import matplotlib.pyplot as plt
import joblib

# Load dataset
df = pd.read_csv(r"C:\Users\hp\Desktop\ml\downtime testing\Machine Downtime.csv")  # Replace with your dataset path

# Map downtime to binary labels
downtime_label_mapping = {"No_Machine_Failure": 0, "Machine_Failure": 1}
df["Downtime_temp"] = df["Downtime"].map(downtime_label_mapping)

# Define feature and target columns
features = [
    "Hydraulic_Pressure(bar)", "Coolant_Pressure(bar)", "Air_System_Pressure(bar)", 
    "Coolant_Temperature", "Hydraulic_Oil_Temperature(?C)", 
    "Spindle_Bearing_Temperature(?C)", "Spindle_Vibration(?m)", 
    "Tool_Vibration(?m)", "Spindle_Speed(RPM)", "Voltage(volts)", 
    "Torque(Nm)", "Cutting(kN)"
]
target = "Downtime_temp"

# Split data into features (X) and target (y)
X = df[features]
y = df[target]

# Handle missing values
imputer = SimpleImputer(strategy='mean')
X = pd.DataFrame(imputer.fit_transform(X), columns=X.columns)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Normalize features
transformer = PowerTransformer()
X_train = transformer.fit_transform(X_train)
X_test = transformer.transform(X_test)

# Train the Random Forest model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy}")
f1_score = f1_score(y_test, y_pred)
print(f"F1-Score: {f1_score}")
print("Classification Report:")
print(classification_report(y_test, y_pred))

# Confusion Matrix
conf_matrix = confusion_matrix(y_test, y_pred)
sns.heatmap(conf_matrix, annot=True, fmt='g', cmap='Blues', xticklabels=["No_Machine_Failure", "Machine_Failure"], yticklabels=["No_Machine_Failure", "Machine_Failure"])
plt.xlabel("Predicted Label")
plt.ylabel("True Label")
plt.title("Confusion Matrix")
plt.show()
print('trying to save')
# Save the trained model and preprocessing components
joblib.dump(model, "machine_downtime_model.pkl")
joblib.dump(imputer, "imputer.pkl")
joblib.dump(transformer, "transformer.pkl")
print('saved few')
# Save encoder for label decoding
encoder = LabelEncoder()
y_encoded = encoder.fit_transform(df[target])
joblib.dump(encoder, "encoder.pkl")

# Save feature columns
joblib.dump(features, "columns.pkl")

# Feature Importance
importances = pd.Series(model.feature_importances_, index=features).sort_values(ascending=False)
importances.plot(kind="bar", title="Feature Importance")
plt.show()
