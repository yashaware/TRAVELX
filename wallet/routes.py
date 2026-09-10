from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.database import get_db
from db.models import Wallet, WalletTransaction

from wallet.schemas import (
    AddMoneyRequest,
    WalletResponse,
    TransactionResponse
)

from auth.security import get_current_user


# ============================================================
# WALLET ROUTER
# ============================================================

wallet_router = APIRouter(
    prefix="/wallet",
    tags=["Wallet"]
)


# ============================================================
# GET WALLET
# ============================================================

@wallet_router.get(
    "/",
    response_model=WalletResponse
)
def get_wallet(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    wallet = db.query(Wallet).filter(
        Wallet.user_id == current_user["id"]
    ).first()

    # Create wallet automatically
    # if user does not have one.
    if not wallet:

        wallet = Wallet(
            user_id=current_user["id"],
            balance=0.0
        )

        db.add(wallet)
        db.commit()
        db.refresh(wallet)

    return {
        "id": wallet.id,
        "user_id": wallet.user_id,
        "balance": wallet.balance,
        "currency": "INR"
    }


# ============================================================
# ADD MONEY
# ============================================================

@wallet_router.post(
    "/add-money",
    response_model=WalletResponse
)
def add_money(
    data: AddMoneyRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    wallet = db.query(Wallet).filter(
        Wallet.user_id == current_user["id"]
    ).first()

    # Create wallet if it does not exist.
    if not wallet:

        wallet = Wallet(
            user_id=current_user["id"],
            balance=0.0
        )

        db.add(wallet)
        db.flush()

    # Add money
    wallet.balance += data.amount

    # Create transaction record
    transaction = WalletTransaction(
        user_id=current_user["id"],
        transaction_type="credit",
        amount=data.amount,
        description="Wallet top-up",
        balance_after=wallet.balance
    )

    db.add(transaction)

    db.commit()
    db.refresh(wallet)

    return {
        "id": wallet.id,
        "user_id": wallet.user_id,
        "balance": wallet.balance,
        "currency": "INR"
    }


# ============================================================
# GET TRANSACTION HISTORY
# ============================================================

@wallet_router.get(
    "/transactions",
    response_model=list[TransactionResponse]
)
def get_transactions(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    transactions = db.query(
        WalletTransaction
    ).filter(
        WalletTransaction.user_id == current_user["id"]
    ).order_by(
        WalletTransaction.id.desc()
    ).all()

    return transactions