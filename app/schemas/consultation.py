from pydantic import BaseModel


class Consultation(BaseModel):
    id: int | None = None
    date: str
    doctor_id: int
    patient_id: int
    time_slot_id: int
    diagnosis: str
    note: str
    created_at: str | None = None
    updated_at: str | None = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        