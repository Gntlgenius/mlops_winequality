import yaml
import os
import joblib
import json
import numpy as np
from prediction_service.error_and_exceptions import NotInRange, NotInColumn






class input_val_mgt:
    def __init__(self, data, schema_path):
        self.dict_req = data
        self.schema_path = schema_path
        self.range_error = NotInRange
        self.col_error = NotInColumn


    def get_schema(self, schema_path=self.schema_path):
        with open(schema_path) as json_file:
            schema = json.load(json_file)
        return schema


    def col_validation(self, col):
        schema = self.get_schema()
        actual_cols = schema.keys()
        if col not in actual_cols:
            raise self.col_error
        else:
            return True

    def val_validation(self, col, val):
        schema = self.get_schema()
        if not (schema['col']['min'] <= float(self.dict_req['col']) <= schema['col']['max']):
            raise range_error
        else:
            return True

    def validate_input_api(self, request_):
        try:
            for col, val in request_.items():
                if self.col_validation(col):
                    if self.val_validation(col, val):
                        return True
        except Exception as e:
            error = {'error':"Error in class input_val_mgt: "+str(e)}
            return error

    def validate_input_form(self):
        try:
            for col, val in self.data.items():
                if self.col_validation(col):
                    if self.val_validation(col, val):
                        return True
        except Exception as e:
            error = {'error':"Error in class input_val_mgt: "+str(e)}
            return error