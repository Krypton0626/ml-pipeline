// Store prediction history
let predictionHistory = {
    labels: [],
    predictions: [],
    confidences: []
};

// Initialize prediction history chart
const ctx = document.getElementById('predictionHistory').getContext('2d');
const historyChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Prediction Confidence',
            data: [],
            borderColor: '#007bff',
            tension: 0.1
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            y: {
                beginAtZero: true,
                max: 1,
                title: {
                    display: true,
                    text: 'Confidence'
                }
            }
        }
    }
});

// Handle form submission
document.getElementById('predictionForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Collect form data
    const formData = {};
    e.target.querySelectorAll('input').forEach(input => {
        formData[input.name] = input.value;
    });
    
    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        const result = await response.json();
        
        if (result.status === 'success') {
            // Update prediction result display
            const resultDiv = document.getElementById('predictionResult');
            resultDiv.className = 'prediction-result ' + (result.prediction === 1 ? 'fraud' : 'legitimate');
            resultDiv.innerHTML = `
                <h3>Prediction Result:</h3>
                <p>This transaction appears to be <strong>${result.prediction === 1 ? 'FRAUDULENT' : 'LEGITIMATE'}</strong></p>
                <p>Confidence: ${(result.confidence * 100).toFixed(2)}%</p>
            `;
            
            // Update prediction history
            updatePredictionHistory(result);
        } else {
            alert('Error: ' + result.message);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error making prediction. Please try again.');
    }
});

function updatePredictionHistory(result) {
    const timestamp = new Date().toLocaleTimeString();
    
    // Add new data point
    predictionHistory.labels.push(timestamp);
    predictionHistory.predictions.push(result.prediction);
    predictionHistory.confidences.push(result.confidence);
    
    // Keep only last 10 predictions
    if (predictionHistory.labels.length > 10) {
        predictionHistory.labels.shift();
        predictionHistory.predictions.shift();
        predictionHistory.confidences.shift();
    }
    
    // Update chart
    historyChart.data.labels = predictionHistory.labels;
    historyChart.data.datasets[0].data = predictionHistory.confidences;
    historyChart.update();
} 