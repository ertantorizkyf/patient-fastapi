from pydantic import BaseModel


class Patient(BaseModel):
    id: int | None = None
    name: str
    sex: str
    address: str
    phone: str
    email: str
    pob: str
    dob: str
    emergency_contact_name: str
    emergency_contact_phone: str
    emergenct_contact_relationship: str
    created_at: str | None = None
    updated_at: str | None = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        