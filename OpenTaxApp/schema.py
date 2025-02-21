from pydantic import BaseModel
from datetime import date

# Validating the response
class UserTransactionSummary(BaseModel):
    user_id: int
    total_transactions: int
    total_amount: float
    average_transaction_amount: float

