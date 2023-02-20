# -*- coding: utf-8 -*-
"""
Created on Sun Feb 19 15:43:52 2023

@author: tssha
"""

from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import json
import uvicorn
from pyngrok import ngrok
from fastapi.middleware.cors import CORSMiddleware
import nest_asyncio
import warnings
warnings.filterwarnings('ignore')

app = FastAPI()

origins = [""]

app.add_middleware(
    
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class model_input(BaseModel):
    
    Pregnancies: int
    Glucose: int
    BloodPressure: int
    SkinThickness: int
    Insulin: int
    BMI: float
    DiabetesPedigreeFunction: float
    Age: int

diabetes_model = pickle.load(open('diabetes_model.sav', 'rb'))

@app.post('/diabetes_prediction')
def diabetes_pred(input_param: model_input):

    input_data = input_param.json()
    input_dict = json.loads(input_data)

    preg = input_dict['Pregnancies']
    glu = input_dict['Glucose']
    bp = input_dict['BloodPressure']
    skin = input_dict['SkinThickness']
    insulin = input_dict['Insulin']
    bmi = input_dict['BMI']
    dpf = input_dict['DiabetesPedigreeFunction']
    age = input_dict['Age']

    input_values = [preg, glu, bp, skin, insulin, bmi, dpf, age]
    prediction = diabetes_model.predict([input_values])

    if(prediction[0]):
        return "The person is diabetic"
    else:
        return "The person is not diabetic"
    
ngrok_tunnel = ngrok.connect(8000)
print('Public URL: ', ngrok_tunnel.public_url)
nest_asyncio.apply()
uvicorn.run(app, port=8000)