from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import joblib
import numpy as np
import os
import uvicorn
import pandas as pd

# Cargar el modelo
modelo = joblib.load('modelo_alzheimer.pkl')

app = FastAPI()

# Endpoint raíz
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
    Gender: float
    Ethnicity: float
    EducationLevel: float
    BMI: float
    Smoking: float
    AlcoholConsumption: float
    PhysicalActivity: float
    DietQuality: float
    SleepQuality: float
    FamilyHistoryAlzheimers: float
    CardiovascularDisease: float
    Diabetes: float
    Depression: float
    HeadInjury: float
    Hypertension: float
    SystolicBP: float
    DiastolicBP: float
    CholesterolTotal: float
    CholesterolLDL: float
    CholesterolHDL: float
    CholesterolTriglycerides: float
    MMSE: float
    FunctionalAssessment: float
    MemoryComplaints: float
    BehavioralProblems: float
    ADL: float
    Confusion: float
    Disorientation: float
    PersonalityChanges: float
    DifficultyCompletingTasks: float
    Forgetfulness: float

# Endpoint de predicción
@app.post("/predecir")
async def predecir(datos: DatosEntrada):
    entrada = np.array([[  # Convertir datos a array 2D
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

    # Guardar en Excel
    df = pd.DataFrame(entrada, columns=datos.__annotations__.keys())
    archivo_excel = "registro_usuarios.xlsx"
    if os.path.exists(archivo_excel):
        df_existente = pd.read_excel(archivo_excel)
        df_nuevo = pd.concat([df_existente, df], ignore_index=True)
    else:
        df_nuevo = df
    df_nuevo.to_excel(archivo_excel, index=False)

    # Predicción
    probabilidad = modelo.predict_proba(entrada)[0][1] * 100
    return {"probabilidad_alzheimer": round(probabilidad, 2)}

# 🆕 Endpoint para descargar el Excel
@app.get("/descargar_excel")
async def descargar_excel():
    archivo = "registro_usuarios.xlsx"
    if os.path.exists(archivo):
        return FileResponse(archivo, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', filename=archivo)
    else:
        return {"error": "El archivo no existe"}

# Ejecutar localmente o en Railway
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("api_modelo:app", host="0.0.0.0", port=port)
