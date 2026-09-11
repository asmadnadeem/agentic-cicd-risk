import time
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.build_graph import agent_app

def benchmark_direct():
    start_time = time.time()
    
    initial_state = {
        "recent_changes": "Updated auth_middleware.js token parsing logic",
        "retrieved_context": "",
        "risk_analysis": "",
        "generated_test_code": ""
    }
    
    agent_app.invoke(initial_state)
    
    end_time = time.time()
    return end_time - start_time

if __name__ == "__main__":
    durations = [benchmark_direct() for _ in range(3)]
    avg_duration = sum(durations) / len(durations)
    print(f"Direct Execution Avg Time: {avg_duration:.2f} seconds")