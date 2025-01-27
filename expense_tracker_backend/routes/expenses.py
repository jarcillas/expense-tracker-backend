from fastapi import APIRouter, Depends
from ..database import SessionLocal
from ..schemas import ExpenseCreate, ExpenseOut
from ..crud import create_expense, get_expenses
from ..auth import get_current_user
from ..models import User

router = APIRouter()


@router.post("/expenses/", response_model=ExpenseOut)
def add_expense(expense: ExpenseCreate, current_user: User = Depends(get_current_user)):
    db = SessionLocal()
    return create_expense(db, expense, current_user.id)


@router.get("/expenses/", response_model=list[ExpenseOut])
def list_expenses(
    skip: int = 0, limit: int = 10, current_user: User = Depends(get_current_user)
):
    db = SessionLocal()
    return get_expenses(db, current_user.id, skip=skip, limit=limit)
