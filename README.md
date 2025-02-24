# OpenTax API & ETL

## Overview
This project contains an ETL pipeline and API service for managing transactions using Apache Airflow and FastAPI. 
The entire setup runs on Docker Desktop.

## Prerequisites
- Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) for your operating system.
- Ensure that `docker-compose` is available in your environment.

## Project Structure
```
OpenTaxProject/
│dags # Airflow Dags Definition
│   ── data/ # Finanacial_transactions.csv   
│── OpenTaxApp/  # FastAPI application source code
│    ── databse_service/ # database service
│    ── models/ # database models
│    ── routers/ # API Endpoint Definitions
│    ── schemas/ # API Validation Schemas
│── OpenTaxEtl/              # Apache Airflow DAGs and configurations
│── docker-compose-opentaxapp.yaml  # Docker Compose configuration
│── README.md                # Documentation
```

## Setup & Running the Project

### 1. Clone the Repository
```sh
git clone <your-repo-url>
cd OpenTaxProject
```

### 2. Start the Services
Run the following command to build and start the required services:
```sh
docker-compose -f docker-compose-opentaxapp.yaml up --build
```
This will start the following services:
- PostgreSQL Database (Port: 5432)
- FastAPI Service (Port: 6000)
- Apache Airflow (Web UI: 8080)

### 3. Verify Setup
#### Check FastAPI

Open a Postman API testing tool and visit:
```
http://localhost:6000/
```
Expected Response:
```json
{"message": "Welcome to the OpenTax API Solution"}
```

#### Check Airflow
Open a browser and visit:
```
http://localhost:8080/
```
Default Credentials for Airflow UI login:
- **Username:** airflow
- **Password:** admin

Default Credentials for AirFlow and Postgres Database Connection:
- **Username:** airflow_adsum
- **Password:** admin_adsum
- **Host** postgres
- **Port*** 5432
- **Database** opentaxdb

## API Endpoint
###  Database Health Check
**GET** `/db_health`
Tests the database connection.

### Transaction Model
The `Transaction` model represents a financial transaction:
```python
class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    transaction_id = Column(String(50), unique=True, nullable=False)
    user_id = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)
    transaction_date = Column(Date, nullable=False)
```

## Stopping the Services
To stop the running containers, use:
```sh
docker-compose -f docker-compose-opentaxapp.yaml down
```

## Troubleshooting
- If you encounter permission issues on Linux, set the required `AIRFLOW_UID` variable before running Docker Compose:
  ```sh
  export AIRFLOW_UID=$(id -u)
  ```
- Ensure all ports (5432, 6000, 8080) are free before starting the services.

## Additional Notes
- PostgreSQL data persists in a Docker volume named `postgres-db-volume`.
- The FastAPI service interacts with the PostgreSQL database using SQLAlchemy.

For any issues oe enquiries contact: malatjim04@gmailcom

---
**Author:** Moshekwa Matthews Malatji


