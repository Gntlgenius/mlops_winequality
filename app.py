from flask import Flask, render_template, request, jsonify
import os
import numpy as np
from src.get_data import read_params
import joblib

from prediction_service.prediction import predictor



params_path = "params.yaml"
webapp_root ="webapp"
my_predictor = predictor()

static_dir = os.path.join(webapp_root, "static")
template_dir = os.path.join(webapp_root, "templates")

app = Flask(__name__, static_folder=static_dir, template_folder=template_dir)



@app.route("/", methods =['POST','GET'])
def home():
    if request.method =="POST":
        try:
            if request.form:
                values = dict(request.form).values()
                data = [list(map(float, values))]
                pred = predictor(data) #object initialization
                response = pred.form_response() #function calling
                return render_template("index.html", response=response)
            elif request.json:
                data = request.json
                pred = predictor(data) #object initialization
                response = pred.api_response()
                return jsonify(response)
                
        except Exception as e:
            print(e)
            error = {"error":"something went wrong"}
            return render_template("404.html", error = error)

    else:
        return render_template("index.html")



if __name__=="__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)


