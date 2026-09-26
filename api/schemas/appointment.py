"""Schemas Pydantic da entidade Appointment.

Define os formatos de entrada e saída usados pelas rotas de consulta,
além das funções que convertem instâncias de Appointment em
dicionários prontos para serialização JSON.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime
from infra.models.appointment import Appointment


def validar_formato_data(value: str) -> str:
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        raise ValueError("date deve estar no formato 'YYYY-MM-DD' (ex: '2026-08-15')")
    return value


class AppointmentSchema(BaseModel):
    """ Define como uma nova consulta a ser inserida deve ser representada.
    """
    patient_id: int = Field(..., examples=[1])
    date: str = "2026-05-20"
    reason: str = "Consulta de rotina"
    notes: Optional[str] = "Paciente relatou dor leve"

    @field_validator("date")
    @classmethod
    def validate_date(cls, value):
        return validar_formato_data(value)


class AppointmentPathSchema(BaseModel):
    """ Define o parâmetro de caminho usado em /appointment/{appointment_id}.
    """
    appointment_id: int


class AppointmentPatientPathSchema(BaseModel):
    """Parâmetro usado para buscar consultas de um paciente."""
    patient_id: int


class AppointmentViewSchema(BaseModel):
    """ Define como uma consulta será retornada.
    """
    id: int = 1
    patient_id: int = 1
    date: str = "2026-08-15"
    reason: str = "Consulta de rotina"
    notes: Optional[str] = None


class ListagemAppointmentsSchema(BaseModel):
    """ Define como uma listagem de consultas será retornada.
    """
    appointments: List[AppointmentViewSchema]


class AppointmentBatchQuery(BaseModel):
    patient_ids: str = Field(
        ...,
        description="IDs dos pacientes separados por vírgula. Exemplo: 1,2,3"
    )

class AppointmentDelSchema(BaseModel):
    """ Define a estrutura retornada após remover uma consulta.
    """
    mesage: str
    appointment_id: int


class AppointmentDelAllSchema(BaseModel):
    """ Define a estrutura retornada após remover uma consulta.
    """
    mesage: str
    patient_id: int


def apresenta_appointment(appointment: Appointment):
    return {
        "appointment_id": appointment.appointment_id,
        "patient_id": appointment.patient_id,
        "date": appointment.date.isoformat() if appointment.date else None,
        "reason": appointment.reason,
        "notes": appointment.notes,
    }


def apresenta_appointments(appointments: List[Appointment]):
    result = {
        "appointments": [
            apresenta_appointment(a)
            for a in appointments
        ]
    }
    return result