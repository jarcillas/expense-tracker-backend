from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from .models import Category, Expense, User
from .schemas import ExpenseCreate, UserCreate
from passlib.context import CryptContext

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Create new user
def create_user(db: Session, user: UserCreate) -> User:
    """
    Creates a new user with a given username, email, and password
    """

    # Check if username already exists
    db_user_username_exists = get_user_by_username(db, username=user.username)
    print(db_user_username_exists)
    if db_user_username_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

    # Check if email already exists
    db_user_email_exists = get_user_by_email(db, email=user.email)
    print(db_user_email_exists)
    if db_user_email_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    hashed_password = pwd_context.hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        is_active=True,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_expense(db: Session, expense: ExpenseCreate, user_id: int):
    """
    Creates a new expense with a description, category, and amount
    """

    db_expense = Expense(**expense.model_dump(), owner_id=user_id)
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense


def get_expenses(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    """
    Fetches all the expenses of the current user
    """

    return (
        db.query(Expense)
        .filter(Expense.owner_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_total_expenses(db: Session, user_id: int):
    """
    Fetches the total amount of expenses of the current user
    """

    total = (
        db.query(func.sum(Expense.amount)).filter(Expense.owner_id == user_id).scalar()
    )
    return total or 0.0


def delete_expense(db: Session, expense_id: int, owner_id: int):
    """
    Delete an expense by its ID, ensuring it belongs to the specific user
    """
    db_expense = (
        db.query(Expense)
        .filter(Expense.id == expense_id, Expense.owner_id == owner_id)
        .first()
    )
    if not db_expense:
        return False
    db.delete(db_expense)
    db.commit()
    return True


def get_user_by_username(db: Session, username: str | None) -> User | None:
    """
    Fetch a user from the database by their username.
    """
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str | None) -> User | None:
    """
    Fetch a user from the database by their email.
    """
    return db.query(User).filter(User.email == email).first()


def get_categories(db: Session):
    """
    Fetches all the categories
    """

    return db.query(Category).all()
