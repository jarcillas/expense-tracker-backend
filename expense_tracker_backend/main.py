from fastapi import FastAPI
from expense_tracker_backend.routes import auth, expenses
import uvicorn

app = FastAPI()

app.include_router(auth.router)
app.include_router(expenses.router)


def start():
    uvicorn.run("expense_tracker_backend.main:app", reload=True)
