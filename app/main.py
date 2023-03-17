from fastapi import FastAPI

import app.routers.doctor as doctor
import app.routers.patient as patient
import app.routers.speciality as speciality

app = FastAPI()
app.include_router(doctor.router)
app.include_router(patient.router)
app.include_router(speciality.router)


@app.get("/ping")
async def root():
    return {"message": "Hello World"}
