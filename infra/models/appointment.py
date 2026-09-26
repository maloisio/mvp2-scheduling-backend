"""Modelo de dados do Agendamento.

Define a entidade Appointment e seu relacionamento com Patient,
mapeados via SQLAlchemy para a tabela 'appointment'.
"""

from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from infra.models.base import Base

from sqlalchemy import BigInteger, Column, Date, String, Identity
from sqlalchemy.orm import Mapped


from sqlalchemy import Column, Integer, BigInteger, Date, String


class Appointment(Base):
    __tablename__ = "appointment"
    __table_args__ = {
        "sqlite_autoincrement": True
    }
    
    appointment_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    patient_id = Column(
        BigInteger,
        nullable=False
    )

    date = Column(Date, nullable=False)
    reason = Column(String(200), nullable=False)
    notes = Column(String(300), nullable=True)

    def __init__(self, patient_id, date, reason, notes=None):
        self.patient_id = patient_id
        self.date = date
        self.reason = reason
        self.notes = notes