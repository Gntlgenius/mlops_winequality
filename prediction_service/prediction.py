import yaml
import os
import joblib
import numpy as np
import json
from src.get_data import read_params
from prediction_service.input_check import input_val_mgt
from prediction_service.error_and_exceptions import NotInRange, NotInColumn


params_path = "../params.yaml"
schema_path = "schema.json"

class predictor:
    def __init__(self, data):
        self.data = data
        self.schema_path = schema_path
        self.params = params_path
        self.range_error = NotInRange
        self.col_error = NotInColumn
        self.validat_input = input_val_mgt(self.data, self.schema_path)
    

    def predict(self, input_data):
        if self.validat_input.validate_input():
            config = read_params(self.params)
            model_path = config["model_dir"]
            model = joblib.load(model_path)
            prediction = model.predict(input_data).to_list()[0]
            try:
                if 3 <= prediction <= 8:
                    return prediction
                else:
                    raise self.range_error

            except NotInRange:
                return "Unexpected result"

    def form_response(self):
        if self.validat_input.validate_input():
            response = self.predict(self.data)
            return response


    def api_response(self):
        try:
            if self.validat_input.validate_input():
                data = np.array([list(self.data.json.values())])
                response = self.predict(data)
                response = {'response':response}
            return response
        
        except Exception as e:
            print (e)
            error = {"error": str(e)}
            return error


        

    



    



            
            




    







