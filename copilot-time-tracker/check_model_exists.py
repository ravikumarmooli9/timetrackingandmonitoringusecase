import os

MODEL_PATH = os.path.join(os.getcwd(), 'tracking', 'my_model.pkl')

print("Checking for model at:", MODEL_PATH)
if os.path.exists(MODEL_PATH):
    print("Model file exists!")
else:
    print("Model file NOT found.")