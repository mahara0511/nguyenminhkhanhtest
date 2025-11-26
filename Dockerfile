FROM python:3.10-slim

WORKDIR /app

# Copy dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project
COPY . .

# Command: chạy job 1 lần rồi exit 0
CMD ["python", "main.py"]
