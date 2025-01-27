from sqlalchemy import Boolean, ForeignKey, String, Float, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import List


# Base class for declarative models
class Base(DeclarativeBase):
    pass


# User model
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(Boolean)

    # Relationship to Expense
    expenses: Mapped[List["Expense"]] = relationship(back_populates="owner")


# Category model
class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True)

    # Relationship to Expense
    expenses: Mapped[List["Expense"]] = relationship(back_populates="category")


# Expense model
class Expense(Base):
    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    description: Mapped[str] = mapped_column(String, index=True)
    amount: Mapped[float] = mapped_column(Float)
    date: Mapped[Date] = mapped_column(Date)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))

    # Relationships
    owner: Mapped["User"] = relationship(back_populates="expenses")
    category: Mapped["Category"] = relationship(back_populates="expenses")
