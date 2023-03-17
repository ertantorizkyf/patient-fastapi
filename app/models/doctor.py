from app.database import Base
from sqlalchemy import Column, String, Integer, TIMESTAMP, text
from sqlalchemy.orm import relationship


class Doctor(Base):
    __tablename__ = 'doctors'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    license_no = Column(String, nullable=False)
    speciality_id = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False,
                        server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, nullable=True,
                        onupdate=text("CURRENT_TIMESTAMP"))
    
    speciality = relationship('Speciality', back_populates='doctors')
