from pydantic import BaseModel


class Speciality(BaseModel):
    id: int | None = None
    name: str
    created_at: str | None = None
    updated_at: str | None = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        