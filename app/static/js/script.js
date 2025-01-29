// Initialize variables for tracking response times
let currentResponseTime = null;
let responseTimes = [];
let iterations = [];

// Function to update the current response time graph
function updateCurrentResponseGraph() {
  // Don't update if no response time
  if (currentResponseTime === null) {
    const trace = {
      x: ["Current Request"],
      y: [0],
      type: "bar",
      marker: {
        color: "#cccccc", // Gray for no data
      },
    };

    const layout = {
      title: {
        text: "Current API Response Time",
        font: { size: 24 },
      },
      yaxis: {
        title: "Response Time (seconds)",
        range: [0, 0.01], // Reduced default range
        tickformat: ".4f", // Show 4 decimal places
        nticks: 5, // Limit number of ticks
      },
      margin: { t: 60, r: 20, l: 60, b: 40 },
    };

    const config = {
      responsive: true,
      displayModeBar: false,
    };

    Plotly.newPlot("current-response-plot", [trace], layout, config);
    return;
  }

  const trace = {
    x: ["Current Request"],
    y: [currentResponseTime],
    type: "bar",
    marker: {
      color: "#4CAF50",
    },
  };

  const layout = {
    title: {
      text: "Current API Response Time",
      font: { size: 24 },
    },
    yaxis: {
      title: "Response Time (seconds)",
      range: [0, Math.max(0.01, currentResponseTime * 1.2)], // Adjusted range
      tickformat: ".4f", // Show 4 decimal places
      nticks: 5, // Limit number of ticks
    },
    margin: { t: 60, r: 20, l: 60, b: 40 },
  };

  const config = {
    responsive: true,
    displayModeBar: false,
  };

  Plotly.newPlot("current-response-plot", [trace], layout, config);
}

// Function to update the response time history graph
function updateHistoryGraph() {
  const trace = {
    x: iterations,
    y: responseTimes,
    mode: "lines+markers",
    type: "scatter",
    line: {
      color: "#4CAF50",
      width: 2,
    },
    marker: {
      color: "#45a049",
      size: 8,
    },
  };

  const layout = {
    title: {
      text: "API Response Time History",
      font: { size: 24 },
    },
    xaxis: {
      title: "Iteration",
      gridcolor: "#e1e1e1",
      zeroline: false,
    },
    yaxis: {
      title: "Response Time (seconds)",
      gridcolor: "#e1e1e1",
      zeroline: false,
    },
    margin: { t: 60, r: 20, l: 60, b: 40 },
  };

  const config = {
    responsive: true,
    displayModeBar: false,
  };

  Plotly.newPlot("response-history-plot", [trace], layout, config);
}

// Update both graphs
function updateGraphs() {
  updateCurrentResponseGraph();
  updateHistoryGraph();
}

// Function to display transaction details
function displayTransactionDetails(features) {
  const detailsDiv = document.getElementById("transaction-details");
  let detailsHTML = "<h3>Transaction Details:</h3><div class='features-grid'>";

  for (const [key, value] of Object.entries(features)) {
    detailsHTML += `
            <div class="feature-item">
                <span class="feature-label">${key}:</span>
                <span class="feature-value">${parseFloat(value).toFixed(
                  6
                )}</span>
            </div>
        `;
  }

  detailsHTML += "</div>";
  detailsDiv.innerHTML = detailsHTML;
}

// Function to make prediction request
async function makePrediction(features) {
  const startTime = performance.now();

  try {
    // Ensure Time field is present
    const featureData = {
      Time: features.Time || 0, // Default to 0 if not present
      Amount: features.Amount,
      ...Object.fromEntries(
        Array.from({ length: 28 }, (_, i) => [
          `V${i + 1}`,
          features[`V${i + 1}`],
        ])
      ),
    };

    console.log("Sending prediction request with features:", featureData);

    const response = await fetch("/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(featureData),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(
        errorData.message || `HTTP error! status: ${response.status}`
      );
    }

    const data = await response.json();
    console.log("Received prediction response:", data);

    const endTime = performance.now();
    currentResponseTime = (endTime - startTime) / 1000;

    // Add to history
    iterations.push(iterations.length + 1);
    responseTimes.push(currentResponseTime);

    console.log("Response time:", currentResponseTime);

    return data;
  } catch (error) {
    console.error("Prediction request failed:", error);
    throw error;
  }
}

// Handle predict button click
document
  .getElementById("predict-btn")
  .addEventListener("click", async function () {
    const button = this;
    button.disabled = true;
    const resultDiv = document.getElementById("predictionResult");

    try {
      // Reset current response time but keep history
      currentResponseTime = null;
      updateGraphs();

      // Get random transaction
      console.log("Fetching random transaction...");
      const randomResponse = await fetch("/get_random_data");
      if (!randomResponse.ok) {
        throw new Error(
          `Failed to fetch random data: ${randomResponse.status}`
        );
      }

      const randomData = await randomResponse.json();
      console.log("Received random data:", randomData);

      if (randomData.status !== "success") {
        throw new Error(
          randomData.message || "Failed to get random transaction"
        );
      }

      // Display transaction details
      displayTransactionDetails(randomData.data);

      // Make prediction
      const predictionData = await makePrediction(randomData.data);

      // After prediction
      updateGraphs();

      if (predictionData.status === "success") {
        const predictionText =
          predictionData.prediction === 1 ? "Fraudulent" : "Legitimate";
        const predictionClass =
          predictionData.prediction === 1 ? "fraud" : "legitimate";

        resultDiv.innerHTML = `
                    <div class="prediction-result ${predictionClass}">
                        <h3>Prediction Result</h3>
                        <p>Transaction is: <strong>${predictionText}</strong></p>
                        <p>Confidence: ${(
                          predictionData.confidence * 100
                        ).toFixed(2)}%</p>
                        <p>Response Time: ${currentResponseTime.toFixed(
                          4
                        )} seconds</p>
                    </div>
                `;
      } else {
        throw new Error(predictionData.message || "Prediction failed");
      }
    } catch (error) {
      console.error("Error during prediction:", error);
      resultDiv.innerHTML = `
                <div class="prediction-result error">
                    <h3>Error</h3>
                    <p>An error occurred: ${error.message}</p>
                </div>
            `;
    } finally {
      button.disabled = false;
    }
  });

// Initialize empty graphs on page load
document.addEventListener("DOMContentLoaded", function () {
  updateGraphs();
});
