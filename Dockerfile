FROM python:latest
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "financial_data_api.main:app", "--host", "0.0.0.0", "--port", "8000"]