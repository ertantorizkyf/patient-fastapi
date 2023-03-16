from fastapi import FastAPI

import app.routers.patient as patient

app = FastAPI()
app.include_router(patient.router)


@app.get("/ping")
async def root():
    return {"message": "Hello World"}
