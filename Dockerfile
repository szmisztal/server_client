FROM python:3.8-slim

WORKDIR /app

ENV PYTHONPATH="/app/common:/app/server_side:${PYTHONPATH}"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY common ./common
COPY server_side ./server_side

CMD ["python", "server_side/server.py"]
