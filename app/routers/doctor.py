import logging
from fastapi import APIRouter, Depends
from sqlalchemy import exc
from sqlalchemy.orm import joinedload

from app.database import SessionLocal, get_db
from app.models.doctor import Doctor as DoctorModel
from app.models.speciality import Speciality as SpecialityModel
from app.schemas.doctor import Doctor as DoctorSchema

router = APIRouter(
    prefix='/doctors',
    tags=['Doctors']
)


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
    result = db.query(DoctorModel).options(joinedload(DoctorModel.speciality)).get(doctor_id)

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
