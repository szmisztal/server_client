FROM python:3.8-slim

WORKDIR /server

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY common ./common
COPY server_side ./server_side

CMD ["python", "server_side/app.py"]
