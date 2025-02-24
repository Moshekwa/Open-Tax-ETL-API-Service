FROM python:latest
EXPOSE 6000

WORKDIR /app

COPY . .

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install -e .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "6000"]