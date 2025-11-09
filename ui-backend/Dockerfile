FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 5000

ENV AI_BACKEND_URL=http://ai-backend:5001

CMD ["python", "app.py"]
