from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..schemas import Category, ExpenseCreate, ExpenseOut, TotalExpensesOut
from ..crud import (
    create_expense,
    get_categories,
    get_expenses,
    get_total_expenses,
    delete_expense,
)
from ..auth import get_current_user
from ..models import User

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/expenses/", response_model=ExpenseOut)
def add_expense(
    expense: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_expense(db, expense, current_user.id)


@router.get("/expenses/", response_model=list[ExpenseOut])
def list_expenses(
    skip: int = 0,
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_expenses(db, current_user.id, skip=skip, limit=limit)


@router.get("/total/", response_model=TotalExpensesOut)
def get_total(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    total_expenses = get_total_expenses(db, current_user.id)
    return {"total_expenses": total_expenses}


@router.get("/category/", response_model=list[Category])
def get_all_categories(db: Session = Depends(get_db)):
    return get_categories(db)


@router.delete("/expense/{expense_id}")
def delete_user_expense(
    expense_id,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    success = delete_expense(db, expense_id, current_user.id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found or does not belong to the user",
        )
    return {"message": "Expense deleted successfully"}
