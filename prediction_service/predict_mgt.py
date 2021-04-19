from src.get_data import read_params
import os
import joblib
import json
import numpy as np



params_path = "params.yaml"

def predict(data):
    config = read_params(params_path)
    model_path = config["model_dir"]
    model = joblib.load(model_path)
    prediction = model.predict(data)
    return prediction[0]


def api_response(request):
    try:
        data = np.array([list(request.json.values())])
        response = predict(data)
        response = {'response':response}
        return response
    except Exception as e:
        print (e)
        error = {"error":"Something went wrong in api_response"}
        return error
    
    
    return prediction[0]
