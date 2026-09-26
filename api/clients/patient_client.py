import requests
import os

PATIENT_SERVICE_URL = os.getenv(
    "PATIENT_SERVICE_URL",
    "http://127.0.0.1:5000"
)

def get_patient(patient_id):
    response = requests.get(
        f"{PATIENT_SERVICE_URL}/patient/{patient_id}",
        timeout=3
    )

    if response.status_code == 404:
        return None

    response.raise_for_status()

    return response.json()