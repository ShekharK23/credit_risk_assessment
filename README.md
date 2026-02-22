# Credit Risk Assessment

Assessment of credit risk for a person using multiple factors. This project provides a simple web app to input applicant details and get a default vs non-default prediction from a trained CatBoost model.

## Project structure

```
credit_risk_assessment/
├── interface.py          # Flask app and prediction endpoint
├── config.py             # Paths and port configuration
├── utils.py              # Credit risk prediction logic (CREDIT_RISK_ASSESMENT)
├── requirements.txt      # Python dependencies
├── templates/
│   ├── html1.html       # Input form (home page)
│   └── Final.html       # Prediction result page
├── 2.EDA_DQ_CHECK/      # EDA and data quality notebooks/reports
├── 3.Project_Code/      # Model training and artifacts (model, scaling, encoding)
└── 5.Documentation/     # Schema and documentation
```

## Setup

1. **Clone the repository**

   ```bash
   git clone <repo-url>
   cd credit_risk_assessment
   ```

2. **Create a virtual environment (recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app**

   ```bash
   python interface.py
   ```

   The app runs at **http://0.0.0.0:5005** (port is set in `config.py`).

## Usage

- **Home (`/`)**  
  Enter applicant details: age, income, home ownership, employment length, loan intent, loan grade, loan amount, interest rate, percent income, default-on-file flag, and credit history length.

- **Predict (`/Predict`)**  
  Submit the form to get a **Default** or **Non-Default** prediction.

## Dependencies

- **Flask** – Web framework
- **CatBoost** – Trained model for credit risk
- **scikit-learn** – Scaling and preprocessing
- **pandas**, **numpy**, **scipy** – Data handling and numerics

See `requirements.txt` for pinned versions.

## Model artifacts

The app expects these files under `3.Project_Code/` (paths in `config.py`):

- `cb_model.pkl` – Trained CatBoost model
- `Scaling.pkl` – Feature scaling
- `encoded.json` – Encoded categorical mappings

## License

Use as per your project’s terms.
