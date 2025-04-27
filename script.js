document.getElementById("prediccion-form").addEventListener("submit", function(e) {
    e.preventDefault();

    // Recolecta los datos del formulario
    const data = {
        Age: parseFloat(document.getElementById('age').value),
        Gender: parseInt(document.getElementById('gender').value),
        Ethnicity: parseInt(document.getElementById('ethnicity').value),
        EducationLevel: parseFloat(document.getElementById('educationLevel').value),
        BMI: parseFloat(document.getElementById('bmi').value),
        Smoking: parseInt(document.getElementById('smoking').value),
        AlcoholConsumption: parseInt(document.getElementById('alcoholConsumption').value),
        PhysicalActivity: parseInt(document.getElementById('physicalActivity').value),
        DietQuality: parseInt(document.getElementById('dietQuality').value),
        SleepQuality: parseInt(document.getElementById('sleepQuality').value),
        FamilyHistoryAlzheimers: parseInt(document.getElementById('familyHistoryAlzheimers').value),
        CardiovascularDisease: parseInt(document.getElementById('cardiovascularDisease').value),
        Diabetes: parseInt(document.getElementById('diabetes').value),
        Depression: parseInt(document.getElementById('depression').value),
        HeadInjury: parseInt(document.getElementById('headInjury').value),
        Hypertension: parseInt(document.getElementById('hypertension').value),
        SystolicBP: parseFloat(document.getElementById('systolicBP').value),
        DiastolicBP: parseFloat(document.getElementById('diastolicBP').value),
        CholesterolTotal: parseFloat(document.getElementById('cholesterolTotal').value),
        CholesterolLDL: parseFloat(document.getElementById('cholesterolLDL').value),
        CholesterolHDL: parseFloat(document.getElementById('cholesterolHDL').value),
        CholesterolTriglycerides: parseFloat(document.getElementById('cholesterolTriglycerides').value),
        MMSE: parseFloat(document.getElementById('mmse').value),
        FunctionalAssessment: parseFloat(document.getElementById('functionalAssessment').value),
        MemoryComplaints: parseInt(document.getElementById('memoryComplaints').value),
        BehavioralProblems: parseInt(document.getElementById('behavioralProblems').value),
        ADL: parseFloat(document.getElementById('adl').value),
        Confusion: parseInt(document.getElementById('confusion').value),
        Disorientation: parseInt(document.getElementById('disorientation').value),
        PersonalityChanges: parseInt(document.getElementById('personalityChanges').value),
        DifficultyCompletingTasks: parseInt(document.getElementById('difficultyCompletingTasks').value),
        Forgetfulness: parseInt(document.getElementById('forgetfulness').value)
    };

    // Realiza la solicitud a la API
    fetch('https://mi-api-3-llrw.onrender.com/predecir', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        // Guardar el resultado de la predicción en localStorage
        localStorage.setItem('porcentajePrediccion', data.probabilidad_alzheimer);

        // Redirigir al usuario a la página de resultados
        window.location.href = 'resultado.html';
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Hubo un problema al obtener la predicción. Intenta de nuevo.');
    });
});
