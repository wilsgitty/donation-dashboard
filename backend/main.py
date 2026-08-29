from fastapi import FastAPI
from database import engine, Base
import models
from routers import donors, donations, campaigns, dashboard
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite's default dev server port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(donors.router)

app.include_router(donations.router)

app.include_router(campaigns.router)

app.include_router(dashboard.router)

@app.get("/")
def read_root():
    return {"status": "backend is running", "db": "connected"}