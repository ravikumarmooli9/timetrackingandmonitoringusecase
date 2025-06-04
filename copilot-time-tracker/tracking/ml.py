import joblib
import os
from tracking.models import TimeEntry, Task
from django.contrib.auth import get_user_model
from django.utils import timezone
import datetime

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'my_model.pkl')

def example_predict(input_data):
    """
    Dummy prediction function.
    Replace with actual ML model logic.
    """
    return 0

def predict_task_time(description):
    """
    Dummy function to predict estimated time (in minutes) for a task
    based on description length or keyword match.
    """
    keywords = {
        'report': 120,
        'meeting': 60,
        'email': 15,
        'analysis': 180,
        'call': 30,
    }
    for keyword, minutes in keywords.items():
        if keyword in description.lower():
            return minutes
    return max(10, len(description) // 10)

def predict_task_time_ml(features):
    """
    Predict task time using a real ML model.
    """
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
    model = joblib.load(MODEL_PATH)
    prediction = model.predict([features])
    return prediction[0]