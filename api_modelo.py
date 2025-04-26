from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import numpy as np
import os
import uvicorn

# Carga el modelo
modelo = joblib.load('modelo_alzheimer.pkl')

app = FastAPI()

@app.get("/")
async def root():
    return {"mensaje": "API de predicción de Alzheimer activa"}

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo de entrada
class DatosEntrada(BaseModel):
    Age: float
    Gender: int
    Ethnicity: int
    EducationLevel: float
    BMI: float
    Smoking: int
    AlcoholConsumption: int
    PhysicalActivity: int
    DietQuality: int
    SleepQuality: int
    FamilyHistoryAlzheimers: int
    CardiovascularDisease: int
    Diabetes: int
    Depression: int
    HeadInjury: int
    Hypertension: int
    SystolicBP: float
    DiastolicBP: float
    CholesterolTotal: float
    CholesterolLDL: float
    CholesterolHDL: float
    CholesterolTriglycerides: float
    MMSE: float
    FunctionalAssessment: int
    MemoryComplaints: int
    BehavioralProblems: int
    ADL: int
    Confusion: int
    Disorientation: int
    PersonalityChanges: int
    DifficultyCompletingTasks: int
    Forgetfulness: int

@app.post("/predecir")
async def predecir(datos: DatosEntrada):
    entrada = np.array([[
        datos.Age,
        datos.Gender,
        datos.Ethnicity,
        datos.EducationLevel,
        datos.BMI,
        datos.Smoking,
        datos.AlcoholConsumption,
        datos.PhysicalActivity,
        datos.DietQuality,
        datos.SleepQuality,
        datos.FamilyHistoryAlzheimers,
        datos.CardiovascularDisease,
        datos.Diabetes,
        datos.Depression,
        datos.HeadInjury,
        datos.Hypertension,
        datos.SystolicBP,
        datos.DiastolicBP,
        datos.CholesterolTotal,
        datos.CholesterolLDL,
        datos.CholesterolHDL,
        datos.CholesterolTriglycerides,
        datos.MMSE,
        datos.FunctionalAssessment,
        datos.MemoryComplaints,
        datos.BehavioralProblems,
        datos.ADL,
        datos.Confusion,
        datos.Disorientation,
        datos.PersonalityChanges,
        datos.DifficultyCompletingTasks,
        datos.Forgetfulness
    ]])
    probabilidad = modelo.predict_proba(entrada)[0][1] * 100
    return {"probabilidad_alzheimer": round(probabilidad, 2)}

# 👇 Esta parte es importante para Railway
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Lee el puerto que da Railway
    uvicorn.run("api_modelo:app", host="0.0.0.0", port=port)
