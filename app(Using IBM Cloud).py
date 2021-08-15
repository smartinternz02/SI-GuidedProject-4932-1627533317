

from flask import Flask, request, render_template
from joblib import load
import requests

API_KEY = "_H3nxJFrwLvNB51OFdXzqCPJ9_k_tQIHGqQwqUWTVwSS"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

#**********************************************************

column = load('onehot.save')

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/y_predict', methods=['POST'])
def y_predict():
    x_test = [[x for x in request.form.values()]]
    
    x_test = column.transform(x_test)
    x_test = x_test.toarray()
    x_test = x_test.tolist()
    
    payload_scoring = {"input_data": [{"values": x_test}]}
    
    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/53c3d6d3-d810-4a8d-af84-3f742006366d/predictions?version=2021-08-05', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    pred = response_scoring.json()
    output = pred['predictions'][0]['values'][0][0]
    print('PRICE IN USD: ', output)
    
    return render_template('index1.html', prediction_text = 'Price (In USD): {}'.format(output))


    
if (__name__ == '__main__'):
    app.run(debug=True)