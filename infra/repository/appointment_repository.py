"""Repositório de acesso a dados da entidade Appoitment.

Contém apenas operações de banco de dados (CRUD). Não deve conter
regras de negócio.
"""

from infra import Session
from infra.models import Appointment


def create(appointment: Appointment) -> Appointment:
    session = Session()
    try:
        session.add(appointment)
        session.commit()
        session.refresh(appointment)
        return appointment
    finally:
        session.close()


def find_all():
    session = Session()
    try:
        return session.query(Appointment).all()
    finally:
        session.close()


def find_by_patient_id(patient_id: int):
    session = Session()
    try:
        return session.query(Appointment).filter(
            Appointment.patient_id == patient_id
        ).all()
    finally:
        session.close()


def delete(appointment_id: int) -> bool:
    session = Session()
    try:
        appointment = session.query(Appointment).filter(
            Appointment.appointment_id == appointment_id
        ).first()

        if not appointment:
            return False

        session.delete(appointment)
        session.commit()
        return True
    finally:
        session.close()

        
def delete_all_by_patient(patient_id: int) -> bool:
    session = Session()
    try:
        deleted_count = session.query(Appointment).filter(
            Appointment.patient_id == patient_id
        ).delete(synchronize_session=False)

        session.commit()

        return deleted_count > 0

    finally:
        session.close()
        

def find_by_patient_ids(patient_ids):
    with Session() as session:
        return (
            session.query(Appointment)
            .filter(Appointment.patient_id.in_(patient_ids))
            .all()
        )    