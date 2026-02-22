import config
import json
import pickle
import numpy as np

class CREDIT_RISK_ASSESMENT():
    def __init__(self,person_age,person_income,person_home_ownership,person_emp_length,loan_intent,loan_grade,loan_amnt,loan_int_rate,loan_percent_income,cb_person_default_on_file,cb_person_cred_hist_length):
        self.person_age = person_age
        self.person_income = person_income
        self.person_home_ownership = person_home_ownership
        self.person_emp_length = person_emp_length
        self.loan_intent = loan_intent
        self.loan_grade = loan_grade
        self.loan_amnt = loan_amnt
        self.loan_int_rate = loan_int_rate
        self.loan_percent_income = loan_percent_income
        self.cb_person_default_on_file = cb_person_default_on_file
        self.cb_person_cred_hist_length = cb_person_cred_hist_length

    def load_model(self):
        with open(config.MODEL_PATH_DT,"rb") as f:
            self.model = pickle.load(f)
        with open(config.SCALING_PATH,"rb") as f1:
            self.scaling = pickle.load(f1)
        with open(config.JSON_PATH,"r") as f2:
            self.json_data = json.load(f2)   

    def get_Credit_Risk(self):
        self.load_model()
        array = np.zeros(len(self.json_data["columns"]),dtype=float) 
        array[0] = self.person_age
        array[1] = self.person_income
        array[2] = self.person_emp_length
        array[3] = self.loan_amnt
        array[4] = self.loan_int_rate
        array[5] = self.loan_percent_income
        array[6] = self.json_data["cb_person_default_on_file_val"][self.cb_person_default_on_file]
        array[7] = self.cb_person_cred_hist_length

        person_home_ownership_index = self.json_data["columns"].index(self.person_home_ownership)
        array[person_home_ownership_index] = 1

        loan_intent_1 = "loan_intent_" + self.loan_intent
        loan_intent_index = self.json_data["columns"].index(loan_intent_1)
        array[loan_intent_index] = 1

        loan_grade_1 = "loan_grade_" + self.loan_grade
        loan_grade_index = self.json_data["columns"].index(loan_grade_1)
        array[loan_grade_index] = 1

        array1 = self.scaling.transform([array])
        print("Input Array for Model = ",array1)
        pred_default = self.model.predict(array1)[0]
        return pred_default

if __name__ == "__main__":
    person_age                   = 21
    person_income                = 9600
    person_home_ownership        = "OWN"       
    person_emp_length            = 5.0
    loan_intent                  = "EDUCATION" 
    loan_grade                   = "B"         
    loan_amnt                    = 1000
    loan_int_rate                = 11.14
    loan_percent_income          = 0.1
    cb_person_default_on_file    = "N"
    cb_person_cred_hist_length   = 2
    obj = CREDIT_RISK_ASSESMENT(person_age,person_income,person_home_ownership,person_emp_length,loan_intent,loan_grade,loan_amnt,loan_int_rate,loan_percent_income,cb_person_default_on_file,cb_person_cred_hist_length)
    res = obj.get_Credit_Risk()
    print("Predicted Credit Risk - ",res)