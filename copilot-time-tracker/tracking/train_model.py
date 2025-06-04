import joblib
from sklearn.linear_model import LinearRegression
import numpy as np
import os

# Example training data: description length vs. estimated minutes
X = np.array([[10], [20], [50], [100], [200], [500]])
y = np.array([10, 20, 30, 60, 120, 300])

model = LinearRegression()
model.fit(X, y)

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'my_model.pkl')
joblib.dump(model, MODEL_PATH)

print(f"Model trained and saved to {MODEL_PATH}")
