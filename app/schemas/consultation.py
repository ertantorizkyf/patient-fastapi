from pydantic import BaseModel


class Consultation(BaseModel):
    id: int | None = None
    date: str | None = None
    doctor_id: int | None = None
    patient_id: int | None = None
    time_slot_id: int | None = None
    diagnosis: str | None = None
    note: str | None = None
    created_at: str | None = None
    updated_at: str | None = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        