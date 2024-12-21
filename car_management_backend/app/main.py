from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from car_management_backend.app.routers import garage, car, maintenance

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(garage.router)
app.include_router(car.router)
app.include_router(maintenance.router)
