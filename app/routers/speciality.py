import logging
from fastapi import APIRouter, Depends
from sqlalchemy import or_, exc

from app.database import SessionLocal, get_db
from app.models.doctor import Doctor as DoctorModel
from app.models.speciality import Speciality as SpecialityModel
from app.schemas.speciality import Speciality as SpecialitySchema

router = APIRouter(
    prefix='/specialities',
    tags=['Specialities']
)


@router.get('/')
async def get_all(db: SessionLocal = Depends(get_db), skip: int = 0, limit: int = 100, with_pagination: bool = False, search: str = ''):
    result = db.query(SpecialityModel).filter(
        SpecialityModel.name.like('%' + search + '%'))
    if (with_pagination):
        result = result.offset(skip).limit(limit)
    result = result.all()

    response = {
        'message': 'Speciality data fetched',
        'data': result
    }
    return response


@router.get('/{speciality_id}')
async def get_detail(speciality_id: int, db: SessionLocal = Depends(get_db)):
    result = db.query(SpecialityModel).get(speciality_id)

    response = {
        'message': 'Speciality detail fetched' if result is not None else 'Speciality detail not found',
        'data': result
    }
    return response


@router.post('/')
async def create(speciality: SpecialitySchema, db: SessionLocal = Depends(get_db)):
    new_speciality = SpecialityModel(**speciality.dict())
    db.add(new_speciality)
    try:
        db.commit()
        db.refresh(new_speciality)
    except exc.SQLAlchemyError as e:
        error = str(e.orig)
        logging.error(error)

        response = {
            'message': error,
            'data': None
        }
        return response

    response = {
        'message': 'New speciality data created successfully',
        'data': new_speciality
    }
    return response


@router.delete('/{speciality_id}')
async def delete(speciality_id: int, db: SessionLocal = Depends(get_db)):
    # CHECK IF DATA EXIST
    existing_data = db.query(SpecialityModel).get(speciality_id)
    if existing_data is None:
        response = {
            'message': 'Speciality does not exist',
            'data': None
        }
        return response
    
    # CHECK IF DOCTOR EXIST
    doctor_count = db.query(DoctorModel).filter(DoctorModel.speciality_id == speciality_id).count()
    if doctor_count > 0:
        response = {
            'message': 'There are doctors with this speciality, cannot delete data',
            'data': None
        }
        return response

    # DELETE DATA
    delete_query = db.query(SpecialityModel).filter(SpecialityModel.id == speciality_id)
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
        'message': 'Speciality data deleted successfully',
        'data': None
    }
    return response
