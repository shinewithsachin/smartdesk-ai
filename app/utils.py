import joblib
import os

MODEL_PATH = "app/ml/ticket_classifier.joblib"

if os.path.exists(MODEL_PATH):
    model_pipeline = joblib.load(MODEL_PATH)
else:
    model_pipeline = None

def predict_ticket_info(description: str):
    if not model_pipeline:
        return "General", "Medium" 
    
    
    prediction = model_pipeline.predict([description])
    category = prediction[0][0]
    priority = prediction[0][1]
    
    return category, priority