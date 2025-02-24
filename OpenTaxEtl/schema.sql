CREATE TABLE task_execution_logs (
    id SERIAL PRIMARY KEY,
    dag_id VARCHAR(255) NOT NULL,
    task_id VARCHAR(255) NOT NULL,
    log_level VARCHAR(50) NOT NULL,
    message TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE transactions (
id SERIAL PRIMARY KEY,
transaction_id VARCHAR(50) UNIQUE NOT NULL,
user_id INT NOT NULL,
amount FLOAT NOT NULL,
transaction_date DATE NOT NULL);