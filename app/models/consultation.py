from app.database import Base
from sqlalchemy import Column, String, Integer, Text, Date, TIMESTAMP, text
from sqlalchemy.orm import relationship

class Consultation(Base):
    __tablename__ = 'consultations'
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    doctor_id = Column(Integer, nullable=False)
    patient_id = Column(Integer, nullable=False)
    time_slot_id = Column(Integer, nullable=False)
    diagnosis = Column(String, nullable=True)
    note  = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, nullable=False,
                        server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, nullable=True,
                        onupdate=text("CURRENT_TIMESTAMP"))
    
    patient = relationship('Patient', foreign_keys=[patient_id],
                          primaryjoin='Patient.id == Consultation.patient_id')
    doctor = relationship('Doctor', foreign_keys=[doctor_id],
                          primaryjoin='Doctor.id == Consultation.doctor_id')
    time_slot = relationship('DoctorTimeSlot', foreign_keys=[time_slot_id],
                          primaryjoin='DoctorTimeSlot.id == Consultation.time_slot_id')
