from pydantic import BaseModel


class DoctorTimeSlot(BaseModel):
    id: int | None = None
    doctor_id: int | None = None
    day: str | None = None
    start_time: str | None = None
    end_time: str | None = None
    is_active: int | None = None
    created_at: str | None = None
    updated_at: str | None = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        