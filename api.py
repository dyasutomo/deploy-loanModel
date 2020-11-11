from flask import Flask, jsonify, request, render_template
import lightgbm as lgb
import numpy as np
import pandas as pd

# Flask application
app = Flask(__name__)
app.config["DEBUG"] = False

# Main page
@app.route('/', methods=['GET'])
def home():
    return "<h1>ML Prediction</h1><p>Using LGBM.</p>"

@app.route('/input_form', methods=['GET','POST'])
def input_form():
    return render_template('input.html')

@app.route('/predict', methods=['GET','POST'])
def predict():
    try:
        loan_amnt  = float(request.form['loan_amnt'])
        open_acc   = float(request.form['open_acc'])
        inq_6mths  = float(request.form['inq_6mths'])
        emp_length = float(request.form['emp_length'])
        int_rate   = float(request.form['int_rate'])
        fico_low   = float(request.form['fico_low'])
        lgbm = lgb.Booster(model_file='models/lgbm_simple_model.txt')
        pred = lgbm.predict(np.array([loan_amnt, open_acc, inq_6mths, emp_length, int_rate, fico_low]).reshape(1, -1))[0]
        return 'The probability to pay back loan is %.2f percent' % (100*pred)
    except:
        return "Error: Please provide complete input data to be predicted via /input_form or /input_file"

@app.route('/input_file',methods = ['GET','POST'])
def upload_route_summary():
    if request.method == 'POST':
        file = request.files.get('fileupload')
        df = pd.read_csv(file)
        lgbm = lgb.Booster(model_file='models/lgbm_simple_model.txt')
        pred = lgbm.predict(df)
        pred_str = ''
        for p in pred:
            pred_str += '%.2f, ' % (100*p)
        return 'The probability to pay back loan is ' + pred_str[:-2] + ' percent'
    else:
        return render_template('upload.html')


if __name__ == '__main__':
    app.run()
    #app.run(port=8000)
