from pydantic import BaseModel
from datetime import date

# We add a validation layer at the Database Level
class TransactionBase(BaseModel):
    user_id = int
    transaction_id = str
    amount = float
    transaction_date = date

# Validating the response
class TransactionResponse(TransactionBase):
    user_id = int
    total_transactions = int
    total_amount = float
    average_transaction_amount = float
    #{"userid": 123,
     #"totaltransactions": 50,
     #"totalamount": 10240.50,
     #"averagetransactionamount": 204.81}
    pass
