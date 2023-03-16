from fastapi import APIRouter
from pydantic import BaseModel, Field


class Patient(BaseModel):
    name: str = Field(None, title="patient name", max_length=25)
    address: str


router = APIRouter(
    prefix='/patients',
    tags=['Patients']
)


@router.get('/')
def get_all():
    return {
        "objective": "return all patient data",
    }


@router.get('/{patient_id}')
def get_detail(patient_id: int):
    return {
        "objective": f"return patient detail with id {patient_id}",
    }


@router.post('/')
def create(patient: Patient):
    return {
        "objective": f"create patient using name {patient.name} and address {patient.address}",
    }


@router.put('/{patient_id}')
def update(patient_id: int, patient: Patient):
    return {
        "objective": f"update patient with id {patient_id} using name {patient.name} and address {patient.address}",
    }


@router.delete('/{patient_id}')
def delete(patient_id: int):
    return {
        "objective": f"delete patient with id {patient_id}",
    }
