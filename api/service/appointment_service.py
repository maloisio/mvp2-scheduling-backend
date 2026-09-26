"""Camada de serviço (regras de negócio) da entidade Appointment.

Orquestra o cadastro, consulta e remoção de consultas médicas. É
responsável por validar que uma consulta só pode ser criada para um
paciente existente.
"""

from datetime import datetime

from infra.repository import appointment_repository
from infra.models import Appointment
from exceptions import NotFoundError
from logger import logger

from api.clients.patient_client import get_patient


def add_appointment(patient_id, date, reason, notes=None):
    """Adiciona uma nova consulta vinculada a um paciente existente.
       Lança NotFoundError se o paciente não existir.
    """
    logger.debug(f"Adicionando consulta para o paciente #{patient_id}")

    patient = get_patient(patient_id)

    if not patient:
        error_msg = "Paciente não encontrado na base"
        logger.warning(f"Erro ao adicionar consulta, {error_msg}")
        raise NotFoundError(error_msg)

    appointment = Appointment(
        patient_id=patient_id,
        date=datetime.strptime(date, "%Y-%m-%d").date(),
        reason=reason,
        notes=notes,
    )

    logger.debug(f"Consulta adicionada ao paciente #{patient_id}")
    return appointment_repository.create(appointment)
    

def get_appointments():
    """Retorna todas as consultas cadastradas.
    """
    return appointment_repository.find_all()

def get_appointments_by_patient_id(patient_id):
    """Retorna todas as consultas de um paciente."""
    logger.debug(f"Buscando consultas do paciente #{patient_id}")

    return appointment_repository.find_by_patient_id(patient_id)

def delete_appointment_by_id(appointment_id):
    """Remove uma consulta pelo ID. Lança NotFoundError se não existir.
    """
    logger.debug(f"Deletando consulta #{appointment_id}")

    appointmentDeleted = appointment_repository.delete(appointment_id)

    if not appointmentDeleted:
        error_msg = "Consulta não encontrada na base"
        logger.warning(f"Erro ao deletar consulta #{appointment_id}, {error_msg}")
        raise NotFoundError(error_msg)

    logger.debug(f"Consulta #{appointment_id} removida")
    return appointment_id

def delete_all_by_patient(patient_id):
    """Remove todas consultas pelo Patient ID. Lança NotFoundError se não existir.
    """
    logger.debug(f"Deletando consultas Paciente #{patient_id}")

    appointmentDeleted = appointment_repository.delete_all_by_patient(patient_id)

    if not appointmentDeleted:
        error_msg = "Não há consultas encontradas na base para o paciente"
        logger.warning(f"Erro ao deletar consultas Paciente #{patient_id}, {error_msg}")
        raise NotFoundError(error_msg)

    logger.debug(f"Consultas removidas do paciente #{patient_id}")
    return patient_id


def get_appointments_by_patient_ids(patient_ids):
    return appointment_repository.find_by_patient_ids(patient_ids)