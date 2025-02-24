from pydantic import BaseModel

# Validating the response
class UserTransactionSummary(BaseModel):
    user_id: int
    total_transactions: int
    total_amount: float
    average_transaction_amount: float

    class Config:
        extra = "forbid"  # Ensuring we dont pass extra fields in the response