from pydantic import BaseModel, Field


class AddMoneyRequest(BaseModel):
    amount: float = Field(gt=0, le=1000000)


class WalletResponse(BaseModel):
    id: int
    user_id: int
    balance: float
    currency: str = "INR"


class TransactionResponse(BaseModel):
    id: int
    user_id: int
    transaction_type: str
    amount: float
    description: str
    balance_after: float