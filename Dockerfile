FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
	&& pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

EXPOSE 8000

# Run FastAPI app with uvicorn (Swagger/OpenAPI auto-enabled)
CMD ["uvicorn", "assistant.run:app", "--host", "0.0.0.0", "--port", "8000"]
