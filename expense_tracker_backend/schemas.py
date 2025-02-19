from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date


# Base schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


# User schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


# Category schemas
class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    id: int

    class Config:
        orm_mode = True


# Expense schemas
class ExpenseBase(BaseModel):
    description: str
    amount: float
    date: date
    category_id: int


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseUpdate(BaseModel):
    description: Optional[str] = None
    amount: Optional[float] = None
    category_id: Optional[int] = None


class ExpenseDelete(ExpenseBase):
    pass


class Expense(ExpenseBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


# Response schemas
class ExpenseOut(Expense):
    category: Category


class UserWithExpenses(User):
    expenses: List[ExpenseOut] = []


class TotalExpensesOut(BaseModel):
    total_expenses: float


# Pagination schema
class PaginatedResponse(BaseModel):
    total_items: int
    total_pages: int
    current_page: int
    items: List[ExpenseOut]
