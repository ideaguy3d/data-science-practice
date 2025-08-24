FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY housing_model.joblib ./
COPY app_regression.py ./app.py
EXPOSE 8080
CMD ["python", "app.py"]
