from app.database import Base
from sqlalchemy import Column, String, Integer, TIMESTAMP, text


class Speciality(Base):
    __tablename__ = 'specialities'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False,
                        server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, nullable=True,
                        onupdate=text("CURRENT_TIMESTAMP"))
