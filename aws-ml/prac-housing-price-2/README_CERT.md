# AWS-focused deployment guidance (cert-friendly)

Recommended for the exam:
- Prefer **SageMaker real-time endpoints** or **Serverless Inference** for online predictions.
- Use **SageMaker Pipelines** for orchestration and **Model Registry** for approvals.
- Use **Data Capture** and **Model Monitor** for drift and quality checks.

Steps (SageMaker real-time):
1. Upload the model to S3:
   aws s3 cp housing_model.joblib s3://<your-bucket>/models/housing_model.joblib
2. Create a SageMaker Model with the scikit-learn inference image for your region.
3. Point model_data to s3://<your-bucket>/models/housing_model.joblib
4. Create EndpointConfig and Endpoint. Set instance type to something small (e.g., ml.t3.medium) for demo.
5. Invoke the endpoint with JSON: {"instances": [[...features in column order...]]}

Alternative:
- **ECS Fargate** with this Dockerfile when you need generic containers.
- **Batch Transform** for offline scoring (cost-friendly for large, infrequent jobs).

Local testing:
- python -m venv .venv && source .venv/bin/activate
- pip install -r requirements.txt
- python -c "import joblib; m=joblib.load('housing_model.joblib'); import numpy as np; print(m.predict(np.zeros((1,10))))"
