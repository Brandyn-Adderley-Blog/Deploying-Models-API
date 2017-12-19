import os
import pandas as pd
import dill as pickle
import numpy as np
import json
from django.shortcuts import render
from django.http import HttpResponse
#from sklearn.externals import joblib


# Create your views here.

#Data input to run predictions on will be a json dataframe

#Load the model
print(' Model being loaded....')
filename = 'model_v2.pk'
with open('./Model-Builds/'+filename, 'rb') as f:
    model = pickle.load(f)
print('Model ' + filename +  ' loaded...')

#Joblib way -- Doesnt work. Causes error.
#model = joblib.load('./Model-Builds/model2.pkl')

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
    print('Predictions done...')
    print(prediction)
    #NP arrays cant be JSON Serialized
    list_predictions = prediction.tolist()

    return HttpResponse(json.dumps(list_predictions))


def predict_proba(request, dataframe):
    data = pd.read_json(dataframe, orient='records')
    prediction = model.predict_proba(data)
    return HttpResponse(json.dumps(prediction))
