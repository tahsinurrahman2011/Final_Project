import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from flask import Flask, jsonify, render_template, request
from joblib import load
import model.persist
from model.persist import load_model



app= Flask(__name__)


@app.route('/')
def index():
    """
    Display page for users to enter explanatory data
    """
    #return "Testing, testing"
    return render_template("index.html")



@app.route('/predict', methods=["POST"])
def predict_test():
    data = request.json

    col_order = [
        "femaleh", "hhsize", "rural", "Low_education", "Low_income",
        "Sumatra", "Java and Bali", "Kalimantan", "Sulawesi", "Childlabour_05", 
        "age_0t6", "age_7t12", "age_13t15", "age_16t18", "age_19t60", "age_61"
    ]

 # convert femaleh to binary variable
    rename_cols = {
        "femaleh": "femaleh",
    }
    

    if (data["femaleh"] == "female"):
        data["femaleh"] = 1
    else:
        data["femaleh"] = 0
# convert rural to binary variable
    if (data["rural"] == "rural"):
        data["rural"] = 1
    else:
        data["rural"] = 0 
# convert low_education to binary variable
    if (data["Low_education"] == "low education"):
        data["Low_education"] = 1
    else:
        data["Low_education"] = 0
# convert low_income to binary variable
    if (data["Low_income"] == "low income"):
        data["Low_income"] = 1
    else:
        data["Low_income"] = 0

    # convert region to regional dummy variables
    if (data["region"] == "Sumatra"):
        data["Sumatra"] = 1
        data["Java and Bali"] = 0
        data["Kalimantan"] = 0
        data["Sulawesi"] = 0
    elif (data["region"] == "Java"):
        data["Sumatra"] = 0
        data["Java and Bali"] = 1
        data["Kalimantan"] = 0
        data["Sulawesi"] = 0
    elif (data["region"] == "Kalimantan"):
        data["Sumatra"] = 0
        data["Java and Bali"] = 0
        data["Kalimantan"] = 1
        data["Sulawesi"] = 0  
    elif (data["region"] == "Sulawesi"):
        data["Sumatra"] = 0
        data["Java and Bali"] = 0
        data["Kalimantan"] = 0
        data["Sulawesi"] = 1
    elif (data["region"] == "Other"):
        data["Sumatra"] = 0
        data["Java and Bali"] = 0
        data["Kalimantan"] = 0
        data["Sulawesi"] = 0

    del data["region"]


    if (data["Childlabour_05"] == "Yes"):
        data["Childlabour_05"] = 1
    else:
        data["Childlabour_05"] = 0


    # rename columns and sort as per the
    # order columns were trained on
    try:
        df = pd.DataFrame([data]).rename(columns=rename_cols)[col_order]
    except Exception as e:
        print("Error Parsing Input Data")
        print(e)
        return "Error"

    X = df.values   

    model=load_model()

    result = model.predict(X).tolist()

    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(debug=True)

