document.getElementById("prediccion-form").addEventListener("submit", function(e) {
    e.preventDefault();

    // Recolecta los datos del formulario con valores por defecto
    const data = {
        Age: parseFloat(document.getElementById('age').value) || ,
        Gender: parseInt(document.getElementById('gender').value) || 0,
        Ethnicity: parseInt(document.getElementById('ethnicity').value) || 0,
        EducationLevel: parseFloat(document.getElementById('educationLevel').value) || 0,
        BMI: parseFloat(document.getElementById('bmi').value) || 0,
        Smoking: parseInt(document.getElementById('smoking').value) || 0,
        AlcoholConsumption: parseInt(document.getElementById('alcoholConsumption').value) || 0,
        PhysicalActivity: parseInt(document.getElementById('physicalActivity').value) || 0,
        DietQuality: parseInt(document.getElementById('dietQuality').value) || 0,
        SleepQuality: parseInt(document.getElementById('sleepQuality').value) || 0,
        FamilyHistoryAlzheimers: parseInt(document.getElementById('familyHistoryAlzheimers').value) || 0,
        CardiovascularDisease: parseInt(document.getElementById('cardiovascularDisease').value) || 0,
        Diabetes: parseInt(document.getElementById('diabetes').value) || 0,
        Depression: parseInt(document.getElementById('depression').value) || 0,
        HeadInjury: parseInt(document.getElementById('headInjury').value) || 0,
        Hypertension: parseInt(document.getElementById('hypertension').value) || 0,
        SystolicBP: parseFloat(document.getElementById('systolicBP').value) || 0,
        DiastolicBP: parseFloat(document.getElementById('diastolicBP').value) || 0,
        CholesterolTotal: parseFloat(document.getElementById('cholesterolTotal').value) || 0,
        CholesterolLDL: parseFloat(document.getElementById('cholesterolLDL').value) || 0,
        CholesterolHDL: parseFloat(document.getElementById('cholesterolHDL').value) || 0,
        CholesterolTriglycerides: parseFloat(document.getElementById('cholesterolTriglycerides').value) || 0,
        MMSE: parseFloat(document.getElementById('mmse').value) || 0,
        FunctionalAssessment: parseFloat(document.getElementById('functionalAssessment').value) || 0,
        MemoryComplaints: parseInt(document.getElementById('memoryComplaints').value) || 0,
        BehavioralProblems: parseInt(document.getElementById('behavioralProblems').value) || 0,
        ADL: parseFloat(document.getElementById('adl').value) || 0,
        Confusion: parseInt(document.getElementById('confusion').value) || 0,
        Disorientation: parseInt(document.getElementById('disorientation').value) || 0,
        PersonalityChanges: parseInt(document.getElementById('personalityChanges').value) || 0,
        DifficultyCompletingTasks: parseInt(document.getElementById('difficultyCompletingTasks').value) || 0,
        Forgetfulness: parseInt(document.getElementById('forgetfulness').value) || 0
    };

    // Define la URL dependiendo si estás en local o producción
    const URL_API = window.location.hostname === 'localhost'
        ? 'http://127.0.0.1:8000/predecir'
        : 'https://tu-api.railway.app/predecir'; // Reemplaza con el URL real de Railway

    // Realiza la solicitud a la API
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
        // Guardar el resultado de la predicción en localStorage
        localStorage.setItem('porcentajePrediccion', data.probabilidad_alzheimer);

        // Redirigir al usuario a la página de resultados
        window.location.href = 'resultado.html';
    })
    .catch(error => {
        console.error('Error al realizar la predicción:', error);
        alert('Hubo un problema al obtener la predicción. Verifica que la API esté activa e intenta de nuevo.');
    });
});
