from flask import Flask,render_template,jsonify,request
import config
from utils import CREDIT_RISK_ASSESMENT

app = Flask(__name__)

@app.route("/")
def get_home():
    return render_template("html1.html")

@app.route('/Predict', methods=['POST'])
def home():
    person_age = int(request.form['person_age'])
    person_income = int(request.form['person_income'])
    person_home_ownership = request.form['person_home_ownership']
    person_emp_length = int(request.form['person_emp_length'])
    loan_intent = request.form['loan_intent']
    loan_grade = request.form['loan_grade']
    loan_amnt = eval(request.form['loan_amnt'])
    loan_int_rate = eval(request.form['loan_int_rate'])
    loan_percent_income = eval(request.form['loan_percent_income'])
    cb_person_default_on_file = request.form['cb_person_default_on_file']
    cb_person_cred_hist_length = eval(request.form['cb_person_cred_hist_length'])
    obj = CREDIT_RISK_ASSESMENT(person_age,person_income,person_home_ownership,person_emp_length,loan_intent,loan_grade,loan_amnt,loan_int_rate,loan_percent_income,cb_person_default_on_file,cb_person_cred_hist_length)
    res1 = obj.get_Credit_Risk()
    return render_template("Final.html",data=res1)

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=config.PORT_NUM)