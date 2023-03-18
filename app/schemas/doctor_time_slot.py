from pydantic import BaseModel


class DoctorTimeSlot(BaseModel):
    id: int | None = None
    doctor_id: int | None = None
    day: str
    start_time: str
    end_time: str
    created_at: str | None = None
    updated_at: str | None = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        