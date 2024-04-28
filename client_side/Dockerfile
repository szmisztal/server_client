FROM python:3.8-slim
WORKDIR /app
COPY client_side/ .
COPY ../requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "client.py"]
