from fastapi import FastAPI
from expense_tracker_backend.routes import auth, expenses

app = FastAPI()

app.include_router(auth.router)
app.include_router(expenses.router)
