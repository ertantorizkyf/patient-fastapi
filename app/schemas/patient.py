from pydantic import BaseModel


class Patient(BaseModel):
    name: str
    address: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
