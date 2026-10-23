import pandas as pd
import numpy as np
import joblib
import sys
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score

# Anchor paths to the directory where train_model.py is located
MODEL_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(MODEL_DIR, '..'))
sys.path.append(PROJECT_ROOT)

from core.features import extract_features

def main():
    print("1. Loading full dataset...")
    dataset_path = os.path.join(MODEL_DIR, 'dataset.csv')
    
    df = pd.read_csv(dataset_path, sep='\t')
    
    print(f"Dataset loaded with {len(df)} rows.")
    df['target'] = df['Label'].map({'good': 0, 'bad': 1})
    
    print("2. Extracting features from URLs (this will take 2-3 minutes)...")
    features_list = df['URL'].apply(extract_features).tolist()
    
    X = pd.DataFrame(features_list)
    y = df['target']
    
    print("3. Splitting data into Training and Testing sets...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("4. Training the Random Forest Classifier...")
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced', n_jobs=-1)
    rf_model.fit(X_train, y_train)
    
    print("5. Evaluating Model Performance (NFR-1.2)...")
    y_pred = rf_model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    
    print(f"   -> Accuracy: {accuracy * 100:.2f}%")
    print(f"   -> F1-Score: {f1:.4f}")
    
    if accuracy >= 0.90 and f1 >= 0.88:
        print("   ✅ Model meets SRS Performance Requirements (NFR-1.2)!")
    else:
        print("   ⚠️ Model falls short of SRS NFR-1.2 metrics.")

    print("6. Saving the trained model...")
    model_path = os.path.join(MODEL_DIR, 'phishing_rf_model.joblib')
    joblib.dump(rf_model, model_path)
    print(f"Model successfully saved to {model_path}!")

if __name__ == "__main__":
    main()