# Adjust based on your exact app (e.g., python:3.9-slim)
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
# Expose the port your app runs on (e.g., 5000 for Flask, 8501 for Streamlit)
EXPOSE 5000
CMD ["python", "app.py"]