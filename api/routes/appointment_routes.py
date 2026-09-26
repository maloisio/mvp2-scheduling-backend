"""Rotas HTTP da entidade Appointment.

Responsável por receber as requisições, delegar o processamento para
api.service.appointment_service e formatar a resposta HTTP.
"""

from api.schemas.appointment import (
    AppointmentSchema,
    AppointmentViewSchema,
    ListagemAppointmentsSchema,
    AppointmentPatientPathSchema,
    AppointmentDelSchema,
    AppointmentDelAllSchema,
    AppointmentBatchQuery,
    AppointmentPathSchema,
    apresenta_appointment,
    apresenta_appointments,
)
from api.schemas.error import ErrorSchema
from api.service import appointment_service
from exceptions import NotFoundError
from flask import request


def init_appointment_routes(app, appointment_tag):
    """Registra as rotas de Consulta na aplicação.
    """

    @app.post('/appointment', tags=[appointment_tag],
              responses={"200": AppointmentViewSchema, "404": ErrorSchema})
    def add_appointment(body: AppointmentSchema):
        """Adiciona uma nova Consulta vinculada a um Paciente existente
        """
        try:
            appointment = appointment_service.add_appointment(
                patient_id=body.patient_id,
                date=body.date,
                reason=body.reason,
                notes=body.notes,
            )
            return apresenta_appointment(appointment), 200
        except NotFoundError as e:
            return {"mesage": str(e)}, 404

    @app.get('/appointments', tags=[appointment_tag],
             responses={"200": ListagemAppointmentsSchema})
    def get_appointments():
        """Lista todas as Consultas cadastradas
        """
        appointments = appointment_service.get_appointments()
        return apresenta_appointments(appointments), 200


    @app.get("/appointments/batch", tags=[appointment_tag])
    def get_appointments_batch(query: AppointmentBatchQuery):
        """Lista consultas de mais de um paciente
        """
        patient_ids = request.args.get("patient_ids")

        if not patient_ids:
            return {"appointments": []}, 200

        patient_ids = [
            int(patient_id)
            for patient_id in patient_ids.split(",")
        ]

        appointments = appointment_service.get_appointments_by_patient_ids(
            patient_ids
        )

        return apresenta_appointments(appointments), 200


    @app.delete('/appointment/<int:appointment_id>', tags=[appointment_tag],
                responses={"200": AppointmentDelSchema, "404": ErrorSchema})
    def del_appointment(path: AppointmentPathSchema):
        """Remove uma Consulta a partir do ID informado
        """
        try:
            appointment_service.delete_appointment_by_id(path.appointment_id)
            return {"mesage": "Consulta removida", "appointment_id": path.appointment_id}, 200
        except NotFoundError as e:
            return {"mesage": str(e)}, 404


    @app.delete('/appointments/<int:patient_id>', tags=[appointment_tag],
                responses={"200": AppointmentDelAllSchema, "404": ErrorSchema})
    def del_all_appointments(path: AppointmentPatientPathSchema):
        """Remove todas consultas do Patient ID informado
        """
        try:
            appointment_service.delete_all_by_patient(path.patient_id)
            return {"mesage": "Consultas removidas", "patient_id": path.patient_id}, 200
        except NotFoundError as e:
            return {"mesage": str(e)}, 404
        

    @app.get(
        '/appointments/patient/<int:patient_id>',
        tags=[appointment_tag],
        responses={"200": ListagemAppointmentsSchema}
    )
    def get_appointments_by_patient(
        path: AppointmentPatientPathSchema
    ):
        """Lista todas as consultas de um paciente."""

        appointments = appointment_service.get_appointments_by_patient_id(
            path.patient_id
        )

        return apresenta_appointments(appointments), 200