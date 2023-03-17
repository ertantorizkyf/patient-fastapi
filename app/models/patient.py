from app.database import Base
from sqlalchemy import Column, String, Integer, Text, Date, TIMESTAMP, text


class Patient(Base):
    __tablename__ = 'patients'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    sex = Column(String(1), nullable=False)
    address = Column(Text, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    pob = Column(String, nullable=False)
    dob = Column(Date, nullable=False)
    emergency_contact_name = Column(String, nullable=False)
    emergency_contact_phone = Column(String, nullable=False)
    emergency_contact_relationship = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False,
                        server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, nullable=True,
                        onupdate=text("CURRENT_TIMESTAMP"))
