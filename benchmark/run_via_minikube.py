import time
import requests

MINIKUBE_URL = "http://127.0.0.1:45319/generate"

def benchmark_minikube(run_number):
    print(f"--- Starting Minikube Pod Run #{run_number} ---")
    payload = {
        "recent_changes": "Updated auth_middleware.js token parsing logic"
    }
    
    start_time = time.time()
    try:
        response = requests.post(MINIKUBE_URL, json=payload, timeout=120)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Minikube deployment not reachable: {e}")
        return 0
        
    end_time = time.time()
    duration = end_time - start_time
    print(f"--- Finished Minikube Pod Run #{run_number} in {duration:.2f}s ---")
    return duration

if __name__ == "__main__":
    durations = []
    for i in range(1, 4):
        d = benchmark_minikube(i)
        if d > 0:
            durations.append(d)
            
    if durations:
        avg_duration = sum(durations) / len(durations)
        print(f"\n✅ Minikube Execution Avg Time: {avg_duration:.2f} seconds")
    else:
        print("\n❌ Failed to run Minikube benchmark.")