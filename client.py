import requests
import time
import numpy as np
import matplotlib.pyplot as plt

url = "http://127.0.0.1:5000/predict"

# Generate random test data
num_requests = 20
response_times = []

for i in range(num_requests):
    sample_input = np.random.rand(30).tolist()
    start_time = time.time()
    response = requests.post(url, json={"features": sample_input})
    end_time = time.time()

    response_time = end_time - start_time
    response_times.append(response_time)

    print(f"Request {i+1}: {response.json()} in {response_time:.4f} sec")

# Plotting the response times
plt.figure(figsize=(10, 5))
plt.plot(range(1, num_requests + 1), response_times, marker='o')
plt.title('Server Response Time per Request')
plt.xlabel('Request Number')
plt.ylabel('Response Time (seconds)')
plt.grid(True)
plt.show()
