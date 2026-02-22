import os

# Flask app: model artifacts in models/ (cb_model, dt_model, Scaling, encoded)
MODELS_DIR = "models"
MODEL_PATH_DT = os.path.join(MODELS_DIR, "cb_model.pkl")
SCALING_PATH = os.path.join(MODELS_DIR, "Scaling.pkl")
JSON_PATH = os.path.join(MODELS_DIR, "encoded.json")

PORT_NUM = 5005
CSV_PATH = os.path.join("Project_Code", "Credit.csv")