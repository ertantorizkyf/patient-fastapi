import logging
from fastapi import APIRouter, Depends
from sqlalchemy import exc, and_, or_
from sqlalchemy.orm import joinedload

from app.database import SessionLocal, get_db
from app.models.consultation import Consultation as ConsultationModel
from app.models.doctor import Doctor as DoctorModel
from app.models.doctor_time_slot import DoctorTimeSlot as DoctorTimeSlotModel
from app.models.speciality import Speciality as SpecialityModel
from app.schemas.doctor import Doctor as DoctorSchema
from app.schemas.doctor_time_slot import DoctorTimeSlot as DoctorTimeSlotSchema
from app.validators import doctor as DoctorValidator


router = APIRouter(
    prefix='/doctors',
    tags=['Doctors']
)


# DOCTOR
@router.get('/')
def get_all(db: SessionLocal = Depends(get_db), skip: int = 0, limit: int = 100, with_pagination: bool = False, search: str = ''):
    result = db.query(DoctorModel).options(joinedload(DoctorModel.speciality)).filter(
        DoctorModel.name.like('%' + search + '%'))
    if (with_pagination):
        result = result.offset(skip).limit(limit)
    result = result.all()

    response = {
        'message': 'Doctor data fetched',
        'data': result
    }
    return response


@router.get('/{doctor_id}')
def get_detail(doctor_id: int, db: SessionLocal = Depends(get_db)):
    result = db.query(DoctorModel).options(
        joinedload(DoctorModel.speciality)).get(doctor_id)

    response = {
        'message': 'Doctor detail fetched' if result is not None else 'Doctor detail not found',
        'data': result
    }
    return response


@router.post('/')
def create(doctor: DoctorSchema, db: SessionLocal = Depends(get_db)):
    # VALIDATE SPECIALITY
    speciality = db.query(SpecialityModel).get(doctor.speciality_id)
    if speciality is None:
        response = {
            'message': 'Speciality does not exist',
            'data': None
        }
        return response

    # CHECK IF LICENSE NO IS ANOTHER DOCTOR'S LICENSE NO
    doctor_license_no = db.query(DoctorModel).filter(
        DoctorModel.license_no == doctor.license_no).first()
    if doctor_license_no is not None:
        response = {
            'message': f'{doctor.license_no} is {doctor_license_no.name}\'s license no',
            'data': None
        }
        return response

    # CREATE DATA
    new_doctor = DoctorModel(**doctor.dict())
    db.add(new_doctor)
    try:
        db.commit()
        db.refresh(new_doctor)
    except exc.SQLAlchemyError as e:
        error = str(e.orig)
        logging.error(error)

        response = {
            'message': error,
            'data': None
        }
        return response

    response = {
        'message': 'New doctor data created successfully',
        'data': new_doctor
    }
    return response


@router.put('/{doctor_id}')
def update(doctor_id: int, doctor: DoctorSchema, db: SessionLocal = Depends(get_db)):
    # VALIDATE SPECIALITY
    speciality = db.query(SpecialityModel).get(doctor.speciality_id)
    if speciality is None:
        response = {
            'message': 'Speciality does not exist',
            'data': None
        }
        return response

    # CHECK IF DATA EXIST
    existing_doctor = db.query(DoctorModel).get(doctor_id)
    if existing_doctor is None:
        response = {
            'message': 'Doctor does not exist',
            'data': None
        }
        return response

    # CHECK IF LICENSE NO IS ANOTHER DOCTOR'S LICENSE NO
    doctor_license_no = db.query(DoctorModel).filter(and_(
        DoctorModel.license_no == doctor.license_no, DoctorModel.id != doctor_id)).first()
    if doctor_license_no is not None:
        response = {
            'message': f'{doctor.license_no} is {doctor_license_no.name}\'s license no',
            'data': None
        }
        return response

    # UPDATE DATA
    update_data = doctor.dict(exclude_unset=True)
    db.query(DoctorModel).filter(DoctorModel.id == doctor_id).update(update_data,
                                                                     synchronize_session=False)
    try:
        db.commit()
        db.refresh(existing_doctor)
    except exc.SQLAlchemyError as e:
        error = str(e.orig)
        logging.error(error)

        response = {
            'message': error,
            'data': None
        }
        return response

    response = {
        'message': 'Doctor data updated successfully',
        'data': existing_doctor
    }
    return response


@router.delete('/{doctor_id}')
def delete(doctor_id: int, db: SessionLocal = Depends(get_db)):
    # CHECK IF DATA EXIST
    existing_data = db.query(DoctorModel).get(doctor_id)
    if existing_data is None:
        response = {
            'message': 'Doctor does not exist',
            'data': None
        }
        return response

    # DELETE DATA
    delete_query = db.query(DoctorModel).filter(
        DoctorModel.id == doctor_id)
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
        'message': 'Doctor data deleted successfully',
        'data': None
    }
    return response


# DOCTOR TIME SLOT
@router.get('/{doctor_id}/time-slots')
def get_time_slots(doctor_id: int, db: SessionLocal = Depends(get_db)):
    existing_doctor = db.query(DoctorModel).get(doctor_id)
    if existing_doctor is None:
        response = {
            'message': 'Doctor does not exist',
            'data': None
        }
        return response

    result = db.query(DoctorTimeSlotModel).filter(
        DoctorTimeSlotModel.doctor_id == doctor_id).all()

    response = {
        'message': 'Doctor time slots fetched',
        'data': result
    }
    return response


@router.post('/{doctor_id}/time-slots')
def insert_time_slot(doctor_id: int, time_slot: DoctorTimeSlotSchema, db: SessionLocal = Depends(get_db)):
    # FORMAT DATA
    time_slot.day = time_slot.day.title()
    time_slot.doctor_id = doctor_id

    # VALIDATE PAYLOAD
    validation_response = DoctorValidator.validate_time_slot_payload(time_slot)
    if validation_response is not None:
        return validation_response

    # CHECK IF DOCTOR EXIST
    existing_doctor = db.query(DoctorModel).get(doctor_id)
    if existing_doctor is None:
        response = {
            'message': 'Doctor does not exist',
            'data': None
        }
        return response

    # CHECK IF SLOT OVERLAPS WITH EXISTING SLOT
    slot_count = db.query(DoctorTimeSlotModel).filter(
        and_(
            DoctorTimeSlotModel.doctor_id == doctor_id,
            DoctorTimeSlotModel.day == time_slot.day,
            or_(
                and_(
                    time_slot.start_time >= DoctorTimeSlotModel.start_time,
                    time_slot.start_time < DoctorTimeSlotModel.end_time
                ),
                and_(
                    time_slot.end_time > DoctorTimeSlotModel.start_time,
                    time_slot.end_time <= DoctorTimeSlotModel.end_time
                )
            ),
            DoctorTimeSlotModel.is_active == 1
        )
    ).count()
    if slot_count > 0:
        response = {
            'message': 'Current request overlaps with active time slots',
            'data': None
        }
        return response

    # CREATE DATA
    new_time_slot = DoctorTimeSlotModel(**time_slot.dict())
    db.add(new_time_slot)
    try:
        db.commit()
        db.refresh(new_time_slot)
    except exc.SQLAlchemyError as e:
        error = str(e.orig)
        logging.error(error)

        response = {
            'message': error,
            'data': None
        }
        return response

    response = {
        'message': 'New doctor time slot data created successfully',
        'data': new_time_slot
    }
    return response


@router.put('/{doctor_id}/time-slots/{slot_id}/toggle')
def toggle_status(doctor_id: int, slot_id: int, db: SessionLocal = Depends(get_db)):
    # CHECK IF DOCTOR EXIST
    existing_doctor = db.query(DoctorModel).get(doctor_id)
    if existing_doctor is None:
        response = {
            'message': 'Doctor does not exist',
            'data': None
        }
        return response

    # CHECK IF SLOT EXIST
    existing_slot = db.query(DoctorTimeSlotModel).get(slot_id)
    if existing_slot is None:
        response = {
            'message': 'Time slot does not exist',
            'data': None
        }
        return response

    # CHECK IF OVERLAPPING SLOT IF TOGGLE TO ACTIVE
    if not existing_slot.is_active:
        slot_count = db.query(DoctorTimeSlotModel).filter(
            and_(
                DoctorTimeSlotModel.doctor_id == doctor_id,
                DoctorTimeSlotModel.day == existing_slot.day,
                or_(
                    and_(
                        existing_slot.start_time >= DoctorTimeSlotModel.start_time,
                        existing_slot.start_time < DoctorTimeSlotModel.end_time
                    ),
                    and_(
                        existing_slot.end_time > DoctorTimeSlotModel.start_time,
                        existing_slot.end_time <= DoctorTimeSlotModel.end_time
                    )
                ),
                DoctorTimeSlotModel.is_active == 1
            )
        ).count()
        if slot_count > 0:
            response = {
                'message': 'Current request overlaps with active time slots',
                'data': None
            }
            return response

    # UPDATE DATA
    time_slot = DoctorTimeSlotSchema(
        is_active=0 if existing_slot.is_active else 1)
    update_data = time_slot.dict(exclude_unset=True)
    db.query(DoctorTimeSlotModel).filter(DoctorTimeSlotModel.id == slot_id).update(update_data,
                                                                                   synchronize_session=False)
    try:
        db.commit()
        db.refresh(existing_slot)
    except exc.SQLAlchemyError as e:
        error = str(e.orig)
        logging.error(error)

        response = {
            'message': error,
            'data': None
        }
        return response

    response = {
        'message': 'Doctor time slot status toggled successfully',
        'data': existing_slot
    }
    return response


# DOCTOR CONSULTATION
@router.get('/{doctor_id}/consultations')
def get_consultations(doctor_id: int, db: SessionLocal = Depends(get_db)):
    existing_doctor = db.query(DoctorModel).get(doctor_id)
    if existing_doctor is None:
        response = {
            'message': 'Doctor does not exist',
            'data': None
        }
        return response
        
    result = db.query(ConsultationModel).options(joinedload(ConsultationModel.patient), joinedload(
        ConsultationModel.time_slot)).filter(ConsultationModel.doctor_id == doctor_id).all()

    response = {
        'message': 'Doctor consultation data fetched',
        'data': result
    }
    return response
