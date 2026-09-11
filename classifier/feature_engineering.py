import pandas as pd

def engineer_features(input_csv="classifier/raw_runs_data.csv"):
    df = pd.read_csv(input_csv)
    
    # 1 for failure, 0 for success
    df['label'] = df['status'].apply(lambda x: 1 if x == 'failure' else 0)
    
    # Normalize duration
    df['duration_norm'] = (df['duration_seconds'] - df['duration_seconds'].mean()) / df['duration_seconds'].std()
    
    # One-hot encoding for PRs
    df['is_pr'] = df['event_type'].apply(lambda x: 1 if x == 'pull_request' else 0)
    
    features = ['duration_norm', 'is_pr']
    return df[features], df['label']

if __name__ == "__main__":
    X, y = engineer_features()
    print("Features engineered successfully.")