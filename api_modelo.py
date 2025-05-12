from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import joblib
import numpy as np
import os
import uvicorn
from io import BytesIO
import openpyxl
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Cargar el modelo
modelo = joblib.load('modelo_alzheimer.pkl')

app = FastAPI()

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

# ID de la hoja y ruta a credenciales
SPREADSHEET_ID = '1DjawlzyQCW1EU2Vt0aLrcyZ57k9tsC-OboReI1KBHkI'
CREDENTIALS_FILE = 'steel-flare-413420-f6c6b0e5dbf4.json'  # Ruta correcta del archivo de credenciales

# Crear cliente de Google Sheets
def crear_cliente_sheets():
    credentials = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE,
        scopes=['https://www.googleapis.com/auth/spreadsheets']
    )
    servicio = build('sheets', 'v4', credentials=credentials)
    return servicio

# Agregar datos a Google Sheets
def agregar_datos_a_sheet(datos):
    servicio = crear_cliente_sheets()
    rango = 'alzheimer_registros!A2'  # Cambié el rango para empezar desde la fila 2

    valores = [[
        datos.Age, datos.Gender, datos.Ethnicity, datos.EducationLevel, datos.BMI, datos.Smoking,
        datos.AlcoholConsumption, datos.PhysicalActivity, datos.DietQuality, datos.SleepQuality,
        datos.FamilyHistoryAlzheimers, datos.CardiovascularDisease, datos.Diabetes, datos.Depression,
        datos.HeadInjury, datos.Hypertension, datos.SystolicBP, datos.DiastolicBP, datos.CholesterolTotal,
        datos.CholesterolLDL, datos.CholesterolHDL, datos.CholesterolTriglycerides, datos.MMSE,
        datos.FunctionalAssessment, datos.MemoryComplaints, datos.BehavioralProblems, datos.ADL,
        datos.Confusion, datos.Disorientation, datos.PersonalityChanges, datos.DifficultyCompletingTasks,
        datos.Forgetfulness
    ]]  # Los datos a agregar a la hoja de cálculo

    cuerpo = {'values': valores}

    servicio.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=rango,
        valueInputOption="RAW",
        body=cuerpo
    ).execute()

# Endpoint raíz
@app.get("/")
async def root():
    return {"mensaje": "API de predicción de Alzheimer activa"}

# Endpoint de predicción
@app.post("/predecir")
async def predecir(datos: DatosEntrada):
    entrada = np.array([[  # Convertir datos a array 2D
        datos.Age, datos.Gender, datos.Ethnicity, datos.EducationLevel, datos.BMI, datos.Smoking,
        datos.AlcoholConsumption, datos.PhysicalActivity, datos.DietQuality, datos.SleepQuality,
        datos.FamilyHistoryAlzheimers, datos.CardiovascularDisease, datos.Diabetes, datos.Depression,
        datos.HeadInjury, datos.Hypertension, datos.SystolicBP, datos.DiastolicBP, datos.CholesterolTotal,
        datos.CholesterolLDL, datos.CholesterolHDL, datos.CholesterolTriglycerides, datos.MMSE,
        datos.FunctionalAssessment, datos.MemoryComplaints, datos.BehavioralProblems, datos.ADL,
        datos.Confusion, datos.Disorientation, datos.PersonalityChanges, datos.DifficultyCompletingTasks,
        datos.Forgetfulness
    ]])

    agregar_datos_a_sheet(datos)  # Llamamos la función para agregar los datos a Google Sheets

    probabilidad = modelo.predict_proba(entrada)[0][1] * 100  # Predicción
    return {"probabilidad_alzheimer": round(probabilidad, 2)}

# Endpoint para descargar Excel desde Google Sheets
@app.get("/descargar_excel")
async def descargar_excel():
    servicio = crear_cliente_sheets()
    rango = 'alzheimer_registros'

    result = servicio.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=rango
    ).execute()

    valores = result.get('values', [])

    # Crear archivo Excel en memoria
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Datos"

    for fila in valores:
        ws.append(fila)

    output = BytesIO()
    wb.save(output)
    output.seek(0)

    return FileResponse(output,
                        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                        filename="encuesta_alzheimer.xlsx")

# Ejecutar localmente o en Railway
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("api_modelo:app", host="0.0.0.0", port=port)