import logging
from fastapi import APIRouter, Depends
from sqlalchemy import or_, exc

from app.database import SessionLocal, get_db
from app.helpers import general as GeneralHelper
from app.models.patient import Patient as PatientModel
from app.schemas.patient import Patient as PatientSchema
from app.validators import patient as PatientValidator


router = APIRouter(
    prefix='/patients',
    tags=['Patients']
)


@router.get('/')
def get_all(db: SessionLocal = Depends(get_db), skip: int = 0, limit: int = 100, with_pagination: bool = False, search: str = ''):
    result = db.query(PatientModel).filter(
        or_(
            PatientModel.name.like('%' + search + '%'),
            PatientModel.phone.like('%' + search + '%'),
            PatientModel.email.like('%' + search + '%'),
            PatientModel.pob.like('%' + search + '%'),
            PatientModel.address.like('%' + search + '%'),
            PatientModel.emergency_contact_name.like('%' + search + '%'),
            PatientModel.emergency_contact_phone.like('%' + search + '%'),
            PatientModel.emergency_contact_relationship.like(
                '%' + search + '%')
        )
    )
    if (with_pagination):
        result = result.offset(skip).limit(limit)
    result = result.all()

    response = {
        'message': 'Patient data fetched',
        'data': result
    }
    return response


@router.get('/{patient_id}')
def get_detail(patient_id: int, db: SessionLocal = Depends(get_db)):
    result = db.query(PatientModel).get(patient_id)

    response = {
        'message': 'Patient detail fetched' if result is not None else 'Patient detail not found',
        'data': result
    }
    return response


@router.post('/')
def create(patient: PatientSchema, db: SessionLocal = Depends(get_db)):
    # FORMAT DATA
    patient.sex = patient.sex.upper()
    patient.phone = GeneralHelper.phone_formatter(patient.phone)
    patient.emergency_contact_phone = GeneralHelper.phone_formatter(patient.emergency_contact_phone)

    # VALIDATE PAYLOAD
    validation_response = PatientValidator.validate_payload(patient)
    if validation_response is not None:
        return validation_response
    
    # CREATE DATA
    new_patient = PatientModel(**patient.dict())
    db.add(new_patient)
    try:
        db.commit()
        db.refresh(new_patient)
    except exc.SQLAlchemyError as e:
        error = str(e.orig)
        logging.error(error)

        response = {
            'message': error,
            'data': None
        }
        return response

    response = {
        'message': 'New patient data created successfully',
        'data': new_patient
    }
    return response


@router.put('/{patient_id}')
def update(patient_id: int, patient: PatientSchema, db: SessionLocal = Depends(get_db)):
    # FORMAT DATA
    patient.sex = patient.sex.upper()
    patient.phone = GeneralHelper.phone_formatter(patient.phone)
    patient.emergency_contact_phone = GeneralHelper.phone_formatter(patient.emergency_contact_phone)

    # VALIDATE PAYLOAD
    validation_response = patientValidator.validate_payload(patient)
    if validation_response is not None:
        return validation_response
    
    # CHECK IF DATA EXIST
    existing_patient = db.query(PatientModel).get(patient_id)
    if existing_patient is None:
        response = {
            'message': 'Patient does not exist',
            'data': None
        }
        return response

    # UPDATE DATA
    update_data = patient.dict(exclude_unset=True)
    db.query(PatientModel).filter(PatientModel.id == patient_id).update(update_data,
                                                                        synchronize_session=False)
    try:
        db.commit()
        db.refresh(existing_patient)
    except exc.SQLAlchemyError as e:
        error = str(e.orig)
        logging.error(error)

        response = {
            'message': error,
            'data': None
        }
        return response

    response = {
        'message': 'Patient data updated successfully',
        'data': existing_patient
    }
    return response


@router.delete('/{patient_id}')
def delete(patient_id: int, db: SessionLocal = Depends(get_db)):
    # CHECK IF DATA EXIST
    existing_patient = db.query(PatientModel).get(patient_id)
    if existing_patient is None:
        response = {
            'message': 'Patient does not exist',
            'data': None
        }
        return response

    # DELETE DATA
    delete_query = db.query(PatientModel).filter(PatientModel.id == patient_id)
    try:
        delete_query.delete(synchronize_session=False)
        db.commit()
    except exc.SQLAlchemyError as e:
        error = str(e.orig)
        logging.error(error)

        response = {
            'message': error,
            'data': None
        }
        return response

    response = {
        'message': 'Patient data deleted successfully',
        'data': None
    }
    return response
