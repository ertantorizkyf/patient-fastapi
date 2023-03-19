# Patient CRUD with FastAPI and SQLAlchemy
  

## Configuring and Running API

1. Create virtual environment (Windows: `python -m venv venv`)
2. Activate virtual environment (Windows Command Prompt: `venv\Scripts\activate.bat`)
3. Install all modules from requirements file (`pip install -r requirements.txt`)
4. Open .env file and setup database configuration. Database used in this app is mariadb
5. Run `alembic upgrade head` to generate tables into specified database in the previous step
6. Run `uvicorn app.main:app --reload` to start server on port 8000

  
## Current Feature

*Descriptions of each endpoint can be viewed in the `notes.md` file*

1. Patient
	a. Get all patient data
	b. Get patient data by id
	c. Create new patient data
	d. Update patient data
	e. Delete patient data
	f. Get specific patient consultation data
2. Doctor
	a. Get all doctor data
	b. Get doctor data by id
	c. Create new doctor data
	d. Update doctor data
	e. Delete doctor data
	f. Get specific doctor time slot data
	g. Create specific doctor time slot data
	h. Toggle specific doctor time slot active status
	i. Get specific doctor consultation data
3. Consultation
	a. Get all consultation data
	b. Get consultation data by id
	c. Create consultation data
	d. Write consultation diagnosis and note
	e. Delete consultation data
4. Speciality (Medical speciality to be referenced in doctor data)
	a. Get speciality data
	b. Get speciality data by id
	c. Create new speciality data
	d. Update speciality data
	e. Delete speciality data