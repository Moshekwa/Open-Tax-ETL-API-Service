FROM python:latest
EXPOSE 6000

WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# COPY src/ ./src/
COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "6000"]