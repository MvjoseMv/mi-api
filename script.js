document.getElementById("prediccion-form").addEventListener("submit", function(e) {
    e.preventDefault();

    // Función para convertir valores a números decimales y garantizar que no sean NaN
    function parseDecimal(value) {
        let parsedValue = parseFloat(value);
        return isNaN(parsedValue) ? 0 : parsedValue;
    }

    // Recolecta los datos del formulario con valores por defecto
    const data = {
        Age: parseDecimal(document.getElementById('age').value),
        Gender: parseInt(document.getElementById('gender').value) || 0,
        Ethnicity: parseInt(document.getElementById('ethnicity').value) || 0,
        EducationLevel: parseDecimal(document.getElementById('educationLevel').value),
        BMI: parseDecimal(document.getElementById('bmi').value),
        Smoking: parseInt(document.getElementById('smoking').value) || 0,
        AlcoholConsumption: parseDecimal(document.getElementById('alcoholConsumption').value),  // Aquí
        PhysicalActivity: parseDecimal(document.getElementById('physicalActivity').value), // Aquí
        DietQuality: parseDecimal(document.getElementById('dietQuality').value), // Aquí
        SleepQuality: parseDecimal(document.getElementById('sleepQuality').value), // Aquí
        FunctionalAssessment: parseDecimal(document.getElementById('functionalAssessment').value), // Aquí
        FamilyHistoryAlzheimers: parseInt(document.getElementById('familyHistoryAlzheimers').value) || 0,
        CardiovascularDisease: parseInt(document.getElementById('cardiovascularDisease').value) || 0,
        Diabetes: parseInt(document.getElementById('diabetes').value) || 0,
        Depression: parseInt(document.getElementById('depression').value) || 0,
        HeadInjury: parseInt(document.getElementById('headInjury').value) || 0,
        Hypertension: parseInt(document.getElementById('hypertension').value) || 0,
        SystolicBP: parseDecimal(document.getElementById('systolicBP').value),
        DiastolicBP: parseDecimal(document.getElementById('diastolicBP').value),
        CholesterolTotal: parseDecimal(document.getElementById('cholesterolTotal').value),
        CholesterolLDL: parseDecimal(document.getElementById('cholesterolLDL').value),
        CholesterolHDL: parseDecimal(document.getElementById('cholesterolHDL').value),
        CholesterolTriglycerides: parseDecimal(document.getElementById('cholesterolTriglycerides').value),
        MMSE: parseDecimal(document.getElementById('mmse').value),
        MemoryComplaints: parseInt(document.getElementById('memoryComplaints').value) || 0,
        BehavioralProblems: parseInt(document.getElementById('behavioralProblems').value) || 0,
        ADL: parseDecimal(document.getElementById('adl').value),
        Confusion: parseInt(document.getElementById('confusion').value) || 0,
        Disorientation: parseInt(document.getElementById('disorientation').value) || 0,
        PersonalityChanges: parseInt(document.getElementById('personalityChanges').value) || 0,
        DifficultyCompletingTasks: parseInt(document.getElementById('difficultyCompletingTasks').value) || 0,
        Forgetfulness: parseInt(document.getElementById('forgetfulness').value) || 0
    };

    // Depuración: Verifica los datos que estás enviando
    console.log("Datos a enviar:", data);

    // Realiza la solicitud a la API
    const URL_API = window.location.hostname === 'localhost'
         ? 'http://127.0.0.1:8000/predecir'
         : 'https://mi-api-production-1666.up.railway.app/predecir';

    // Realiza la solicitud con fetch
    fetch(URL_API, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Error en la solicitud: ${response.status} ${response.statusText}`);
        }
        return response.json();
    })
    .then(data => {
        console.log("Respuesta de la API:", data);

        if (data && data.probabilidad_alzheimer !== undefined) {
            localStorage.setItem('porcentajePrediccion', data.probabilidad_alzheimer);
            window.location.href = 'resultado.html';
        } else {
            console.error("La respuesta no contiene probabilidad de Alzheimer");
            alert("No se pudo obtener la predicción.");
        }
    })
    .catch(error => {
        console.error('Error al realizar la predicción:', error);
        alert('Hubo un problema al obtener la predicción.');
    });
});