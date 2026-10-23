from core.features import extract_features
import os
import sys
import time
from urllib.parse import urlparse
from flask import Flask, jsonify, render_template, request
import joblib
import pandas as pd
#testing changes
# Anchor all paths to the directory where app.py is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
  sys.path.insert(0, BASE_DIR)

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static"),
)

MODEL_PATH = os.path.join(BASE_DIR, "model", "phishing_rf_model.joblib")
try:
  print("Loading Machine Learning Model...")
  model = joblib.load(MODEL_PATH)
  print("✅ Model loaded successfully.")
except FileNotFoundError:
  print(
      f"⚠️ Error: Model not found at {MODEL_PATH}. Please run train_model.py"
      " first."
  )
  model = None

# INDUSTRY STANDARD FIX: Top Domains Allowlist
# If a URL belongs to one of these domains, it automatically passes.
WHITELIST = [
    "google.com",
    "www.google.com",
    "whatsapp.com",
    "web.whatsapp.com",
    "youtube.com",
    "www.youtube.com",
    "github.com",
    "www.github.com",
    "linkedin.com",
    "www.linkedin.com",
    "microsoft.com",
    "apple.com",
]


@app.route("/")
def index():
  return render_template("index.html")


@app.route("/api/analyze", methods=["POST"])
def analyze():
  if model is None:
    return jsonify({"error": "Machine learning model is not loaded."}), 500

  data = request.get_json()
  if not data or "url" not in data or not data["url"].strip():
    return jsonify({"error": "Invalid input. Please provide a valid URL."}), 400

  raw_url = data["url"]
  start_time = time.time()

  try:
    # Extract the domain to check against our whitelist
    parsed = urlparse(
        raw_url if raw_url.startswith("http") else "http://" + raw_url
    )
    domain = parsed.netloc.lower()

    features_dict = extract_features(raw_url)

    # 1. Check the Whitelist First!
    if domain in WHITELIST:
      verdict = "Safe"
      confidence = 100.00
      print(f"🔒 Whitelist triggered for: {domain}")
    else:
      # 2. If not in whitelist, let the ML Model decide
      features_df = pd.DataFrame([features_dict])
      prediction = model.predict(features_df)[0]
      probabilities = model.predict_proba(features_df)[0]

      verdict = "Phishing" if prediction == 1 else "Safe"
      confidence = round(max(probabilities) * 100, 2)

    processing_time = round((time.time() - start_time) * 1000, 2)

    return jsonify({
        "url": raw_url,
        "verdict": verdict,
        "confidence_score": confidence,
        "features": features_dict,
        "processing_time_ms": processing_time,
    })

  except Exception as e:
    return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000, debug=True)
#testing for CCA3
