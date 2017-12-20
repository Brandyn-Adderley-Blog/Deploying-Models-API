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
    #How to get payload from request?
    print('----------------- JSON ----------------------')
    print(dataframe)
    print('---------------------------------------------')
    data = pd.read_json(dataframe, orient='records')
    print('--------------- DataFrame -------------------')
    print(data.info())
    print('---------------------------------------------')
    print('Doing predictions now..')
    prediction = model.predict(data)
    prediction_prob = model.predict_proba(data)

    print(prediction)
    #NP arrays cant be JSON Serialized
    list_predictions = prediction.tolist()
    list_predictions_prob = prediction_prob.tolist()
    final = list(zip(list_predictions, list_predictions_prob))
    return HttpResponse(json.dumps(final))
