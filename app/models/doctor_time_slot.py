from app.database import Base
from sqlalchemy import Column, String, Integer, TIMESTAMP, text, TIME
from sqlalchemy.orm import relationship


class DoctorTimeSlot(Base):
    __tablename__ = 'doctor_time_slots'
    id = Column(Integer, primary_key=True)
    doctor_id = Column(Integer, nullable=False)
    day = Column(String, nullable=False)
    start_time = Column(TIME, nullable=False)
    end_time = Column(TIME, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False,
                        server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, nullable=True,
                        onupdate=text("CURRENT_TIMESTAMP"))

    doctor = relationship('Doctor', foreign_keys=[doctor_id],
                          primaryjoin='Doctor.id == DoctorTimeSlot.doctor_id')
