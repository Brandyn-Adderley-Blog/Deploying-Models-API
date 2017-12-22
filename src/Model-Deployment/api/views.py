import os
import pandas as pd
import dill as pickle
import numpy as np
import json
from django.shortcuts import render
from django.http import HttpResponse

#Check to see if gunicorn so can slightly change the file path.
is_gunicorn = "gunicorn" in os.environ.get("SERVER_SOFTWARE", "")
print(is_gunicorn)

#Load the model
print(' Model being loaded....')
filename = 'model_v2.pk'
if is_gunicorn:
    with open('../Model-Builds/'+filename, 'rb') as f:
        model = pickle.load(f)
else:
    with open('./Model-Builds/'+filename, 'rb') as f:
        model = pickle.load(f)

print('Model ' + filename +  ' loaded...')

def predict(request, dataframe):
    #Turn payload into dataframe
    print('----------------- JSON ----------------------')
    print(dataframe)
    print('---------------------------------------------')
    data = pd.read_json(dataframe, orient='records')
    print('--------------- DataFrame -------------------')
    print(data.info())
    print('---------------------------------------------')
    print('Doing predictions now..')
    #Perform predictions
    prediction = model.predict(data)
    prediction_prob = model.predict_proba(data)
    #Just want the probablity of class predicted
    predict_prob_class = prediction_prob[:,0]
    print(prediction)
    #Grab index
    index_list = data.index

    #Create DataFrame
    response_df = pd.DataFrame({"Prediction":prediction, "Probability":predict_prob_class}, index=index_list)
    response_json = response_df.to_json()
    return HttpResponse(response_json)
