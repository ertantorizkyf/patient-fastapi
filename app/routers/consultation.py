import logging
from fastapi import APIRouter, Depends
from sqlalchemy import exc, and_, or_
from sqlalchemy.orm import joinedload

from app.database import SessionLocal, get_db
from app.models.consultation import Consultation as ConsultationModel
from app.models.doctor import Doctor as DoctorModel
from app.models.doctor_time_slot import DoctorTimeSlot as DoctorTimeSlotModel
from app.models.patient import Patient as PatientModel
from app.schemas.consultation import Consultation as ConsultationSchema
from app.validators import consultation as ConsultationValidator


router = APIRouter(
    prefix='/consultations',
    tags=['Consultations']
)


@router.get('/')
def get_all(db: SessionLocal = Depends(get_db), skip: int = 0, limit: int = 100, with_pagination: bool = False, search: str = ''):
    result = db.query(ConsultationModel).options(joinedload(ConsultationModel.patient), joinedload(ConsultationModel.doctor).joinedload(DoctorModel.speciality), joinedload(ConsultationModel.time_slot)).filter(
        or_(ConsultationModel.diagnosis.like('%' + search + '%'), ConsultationModel.note.like('%' + search + '%')))
    if (with_pagination):
        result = result.offset(skip).limit(limit)
    result = result.all()

    response = {
        'message': 'Consultation data fetched',
        'data': result
    }
    return response


@router.get('/{consultation_id}')
def get_detail(consultation_id: int, db: SessionLocal = Depends(get_db)):
    result = db.query(ConsultationModel).options(joinedload(ConsultationModel.patient), joinedload(
        ConsultationModel.doctor).joinedload(DoctorModel.speciality), joinedload(ConsultationModel.time_slot)).get(consultation_id)

    response = {
        'message': 'Consultation detail fetched' if result is not None else 'Consultation detail not found',
        'data': result
    }
    return response


@router.post('/')
def create(consultation: ConsultationSchema, db: SessionLocal = Depends(get_db)):
    # FORMAT PAYLOAD
    consultation.diagnosis = None
    consultation.note = None

    # VALIDATE DOCTOR
    doctor = db.query(DoctorModel).get(consultation.doctor_id)
    if doctor is None:
        response = {
            'message': 'Doctor does not exist',
            'data': None
        }
        return response

    # VALIDATE PATIENT
    patient = db.query(PatientModel).get(consultation.patient_id)
    if patient is None:
        response = {
            'message': 'Patient does not exist',
            'data': None
        }
        return response

    # VALIDATE TIME SLOT
    time_slot = db.query(DoctorTimeSlotModel).get(consultation.time_slot_id)
    if time_slot is None:
        response = {
            'message': 'Time slot does not exist',
            'data': None
        }
        return response
    if not time_slot.is_active:
        response = {
            'message': 'Time slot is not active',
            'data': None
        }
        return response
    consultation_date_validation_response = ConsultationValidator.validate_consulation_date(
        consultation, time_slot)
    if consultation_date_validation_response is not None:
        return consultation_date_validation_response

    # CHECK IF DOCTOR AND TIME SLOT MATCH
    if doctor.id != time_slot.doctor_id:
        response = {
            'message': 'Doctor and time slot do not active',
            'data': None
        }
        return response

    # CHECK IF SLOT IS ALREADY USED
    existing_consultation = db.query(ConsultationModel).filter(and_(
        ConsultationModel.time_slot_id == consultation.time_slot_id, ConsultationModel.date == consultation.date)).first()
    if existing_consultation is not None:
        response = {
            'message': 'Time slot has been taken by another consultation',
            'data': None
        }
        return response

    # CREATE DATA
    new_consultation = ConsultationModel(**consultation.dict())
    db.add(new_consultation)
    try:
        db.commit()
        db.refresh(new_consultation)
    except exc.SQLAlchemyError as e:
        error = str(e.orig)
        logging.error(error)

        response = {
            'message': error,
            'data': None
        }
        return response

    response = {
        'message': 'New consultation data created successfully',
        'data': new_consultation
    }
    return response


@router.put('/{consultation_id}/write-diagnosis')
def write_diagnosis(consultation_id: int, consultation: ConsultationSchema, db: SessionLocal = Depends(get_db)):
    # CHECK IF DATA EXIST
    existing_consultation = db.query(ConsultationModel).get(consultation_id)
    if existing_consultation is None:
        response = {
            'message': 'Consultation does not exist',
            'data': None
        }
        return response

    # FORMAT PAYLOAD
    consultation.date = existing_consultation.date
    consultation.doctor_id = existing_consultation.doctor_id
    consultation.patient_id = existing_consultation.patient_id
    consultation.time_slot_id = existing_consultation.time_slot_id

    # CHECK IF DIAGNOSIS HAS BEEN WRITTEN BEFORE
    if existing_consultation.note is not None or existing_consultation.diagnosis is not None:
        response = {
            'message': 'Diagnosis has been written before',
            'data': None
        }
        return response

    # UPDATE DATA
    update_data = consultation.dict(exclude_unset=True)
    db.query(ConsultationModel).filter(ConsultationModel.id == consultation_id).update(update_data,
                                                                                       synchronize_session=False)
    try:
        db.commit()
        db.refresh(existing_consultation)
    except exc.SQLAlchemyError as e:
        error = str(e.orig)
        logging.error(error)

        response = {
            'message': error,
            'data': None
        }
        return response

    response = {
        'message': 'Consultation data updated successfully',
        'data': existing_consultation
    }
    return response


@router.delete('/{consultation_id}')
def delete(consultation_id: int, db: SessionLocal = Depends(get_db)):
    # CHECK IF DATA EXIST
    existing_consultation = db.query(ConsultationModel).get(consultation_id)
    if existing_consultation is None:
        response = {
            'message': 'Consultation does not exist',
            'data': None
        }
        return response

    if existing_consultation.diagnosis is not None or existing_consultation.note is not None:
        response = {
            'message': 'Cannot delete consultation with diagnosis',
            'data': None
        }
        return response

    # DELETE DATA
    delete_query = db.query(ConsultationModel).filter(
        ConsultationModel.id == consultation_id)
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
        'message': 'Consultation data deleted successfully',
        'data': None
    }
    return response
