import os

# Flask app: model artifacts in models/ (cb_model, dt_model, Scaling, encoded)
MODELS_DIR = "models"
MODEL_PATH_DT = os.path.join(MODELS_DIR, "cb_model.pkl")
SCALING_PATH = os.path.join(MODELS_DIR, "Scaling.pkl")
JSON_PATH = os.path.join(MODELS_DIR, "encoded.json")

PORT_NUM = int(os.environ.get("PORT", 5005))
DEBUG = os.environ.get("FLASK_DEBUG", "0").lower() in ("1", "true", "yes")
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-in-production")