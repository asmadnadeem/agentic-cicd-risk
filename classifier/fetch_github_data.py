import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

def fetch_runs(owner="actions", repo="runner", limit=100):
    """Fetches real historical runs from a GitHub repository."""
    url = f"https://api.github.com/repos/{owner}/{repo}/actions/runs?per_page={limit}"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"Bearer {os.getenv('GITHUB_TOKEN')}"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch: {response.text}")
        return
    
    runs = response.json().get("workflow_runs", [])
    data = []
    
    for run in runs:
        status = run.get("conclusion")
        if status in ["success", "failure"]:
            created_at = pd.to_datetime(run.get("created_at"))
            updated_at = pd.to_datetime(run.get("updated_at"))
            duration = (updated_at - created_at).total_seconds()
            
            data.append({
                "run_id": run.get("id"),
                "status": status,
                "duration_seconds": duration,
                "event_type": run.get("event"),
                "actor": run.get("actor", {}).get("login")
            })
            
    df = pd.DataFrame(data)
    df.to_csv("classifier/raw_runs_data.csv", index=False)
    print(f"Saved {len(df)} real runs to raw_runs_data.csv")

if __name__ == "__main__":
    fetch_runs()