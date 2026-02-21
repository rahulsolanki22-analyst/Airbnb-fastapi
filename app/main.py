from fastapi import FastAPI
from .database import engine
from . import models
from .routers import users,listings,bookings

app = FastAPI()

app.include_router(users.router)
app.include_router(listings.router)
app.include_router(bookings.router)

@app.get("/")
def root():
    return {"message": "Airbnb API running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)