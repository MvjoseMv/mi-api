from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib  # o pickle
import numpy as np

# Carga el modelo
modelo = joblib.load('modelo_alzheimer.pkl')  # <-- cambia al nombre de tu modelo

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

# Define tu modelo de entrada
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
    # Convertimos los datos a un array para predecir
    entrada = np.array([
        [
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
        ]
    ])

    # Predecimos usando el modelo
    probabilidad = modelo.predict_proba(entrada)[0][1] * 100  # [0][1] -> Probabilidad de clase "1" (Alzheimer)

    return {"probabilidad_alzheimer": round(probabilidad, 2)}
