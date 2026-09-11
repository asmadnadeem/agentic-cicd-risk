import os
import sys
import json
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score, precision_score, recall_score

# Add project root directory to sys.path to resolve module import issues
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from classifier.feature_engineering import engineer_features

def train_and_evaluate():
    X, y = engineer_features()
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = LogisticRegression()
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    
    metrics = {
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "precision": float(precision_score(y_test, y_pred, zero_division=0)),
        "recall": float(recall_score(y_test, y_pred, zero_division=0)),
        "coefficients": {
            "duration_norm": float(model.coef_[0][0]),
            "is_pr": float(model.coef_[0][1])
        }
    }
    
    os.makedirs("results", exist_ok=True)
    with open("results/classifier_metrics.json", "w") as f:
        json.dump(metrics, f, indent=4)
        
    print("Model trained successfully. Metrics saved to results/classifier_metrics.json.")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, zero_division=0))

if __name__ == "__main__":
    train_and_evaluate()