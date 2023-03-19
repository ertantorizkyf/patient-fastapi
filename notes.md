## Endpoint Documentation


#### Patient

- Description: these endpoints are related to patient data. It allows accessing, creating, updating, and deleting data regarding patients.

- Endpoints:
	-  `GET`  `{base_url}/patients`
		desc: Getting all available patient data from the db. It also allows pagination via query parameter. It also enable searching data by keyword via query parameter.
		available query param:
		-  `with_pagination`  `True/False`
		-  `skip`  `int`
		-  `limit`  `int`
		-  `search`  `string`

	-  `GET`  `{base_url}/patients/{patient_id}`
		desc: Getting patient data from the db based on `patient_id`.

	-  `POST`  `{base_url}/patients`
		desc: Create new patient data and insert it into the db. Phone number will be formatted into with Indonesian prefix (62). Date of birth (dob) must be written in `year-month-date` format. Accepted sex value is either `F` or `M`.
		sample payload:
	
			{
				"name": "Jane",
				"sex": "F",
				"address": "Wall st",
				"phone": "+ 8-5-6",
				"email": "abc@oas.com",
				"pob": "Jakarta",
				"dob": "1998-10-12",
				"emergency_contact_name": "John",
				"emergency_contact_phone": "0432",
				"emergency_contact_relationship": "spouse"
			}

	-  `PUT`  `{base_url}/patients/{patient_id}`
desc: Updating patient data based on `patient_id`. Phone number will be formatted into with Indonesian prefix (62). Date of birth (dob) must be written in `year-month-date` format. Accepted sex value is either `F` or `M`.
	sample payload:

			{
				"name": "Jane",
				"sex": "F",
				"address": "Wall st",
				"phone": "+ 8-5-6",
				"email": "abc@oas.com",
				"pob": "Jakarta",
				"dob": "1998-10-12",
				"emergency_contact_name": "John",
				"emergency_contact_phone": "0432",
				"emergency_contact_relationship": "spouse"
			}
			
	-  `DELETE`  `{base_url}/patients/{patient_id}`
		desc: Deleting patient data based on `patient_id`. Deletion process will fail if `patient_id` exists in consultation data.
	-  `GET`  `{base_url}/patients/{patient_id}/consultations`
		desc: Get consultation data of patient with `patient_id`.

  
#### Speciality

- Description: these endpoints are related to medical speciality data. It allows accessing, creating, and deleting data regarding specialities. Specialities data are needed to insert doctor data as the doctors needed `speciality_id` to be created.

- Endpoints:
	-  `GET`  `{base_url}/specialities`
		desc: Getting all available medical speciality data from the db. It also allows pagination via query parameter. It also enable searching data by keyword via query parameter.
		available query param:
		-  `with_pagination`  `True/False`
		-  `skip`  `int`
		-  `limit`  `int`
		-  `search`  `string`

	-  `GET`  `{base_url}/specialities/{speciality_id}`
		desc: Getting speciality data from the db based on `speciality_id`.

	-  `POST`  `{base_url}/specialities`
		desc: Create new speciality data and insert it into the db.	
		sample payload:
	
			{
				"name": "General Practitioner"
			}
			
	-  `DELETE`  `{base_url}/specialities/{speciality_id}`
		desc: Deleting speciality data based on `speciality_id`. Deletion process will fail if `speciality_id` exists in doctor data.

  
#### Doctor

- Description: these endpoints are related to doctor data. It allows accessing, creating, updating, and deleting data regarding doctors and their time slots. Doctor time slots will be needed in order to create consultation data.

- Endpoints:
	-  `GET`  `{base_url}/doctors`
		desc: Getting all available doctor data from the db. It also allows pagination via query parameter. It also enable searching data by keyword via query parameter.
		available query param:
		-  `with_pagination`  `True/False`
		-  `skip`  `int`
		-  `limit`  `int`
		-  `search`  `string`

	-  `GET`  `{base_url}/doctors/{doctor_id}`
		desc: Getting doctor data from the db based on `doctor_id`.

	-  `POST`  `{base_url}/doctors`
		desc: Create new doctor data and insert it into the db. `license_no` is unique and can only be assigned to one doctor.
		sample payload:
	
			{
				"name": "John",
				"speciality_id":  1,
				"license_no":  "102030"
			}

	-  `PUT`  `{base_url}/doctors/{doctor_id}`
		desc: Update doctor data based on `doctor_id`. `license_no` is unique and can only be assigned to one doctor.
		sample payload:
	
			{
				"name": "John",
				"speciality_id":  1,
				"license_no":  "102030"
			}
			
	-  `DELETE`  `{base_url}/doctors/{doctor_id}`
		desc: Deleting doctor data based on `speciality_id`. Deletion process will fail if `doctor_id` exists in consultation data.

	-  `GET`  `{base_url}/doctors/{doctor_id}/time-slots`
		desc: Getting doctor time slot data from the db based on `doctor_id`.
		
-  `POST`  `{base_url}/doctors/{doctor_id}/time-slots`
		desc: Create new doctor time slot data based on `doctor_id`. Accepted `day` values are day names in English and written in title case. Creation will fail if the payload overlaps with existing doctor time slot of said doctor.
		sample payload:
	
			{
				"day": "Monday",
				"start_time":  "08:00",
				"end_time":  "09:00"
			}

	-  `PUT`  `{base_url}/doctors/{doctor_id}/time-slots/{slot_id}/toggle`
		desc: Toggling doctor time slot data between `active` or `inactive`. It is defined by the `is_active` column in the db table. Inactive slots can't be assigned to a consultation data.
  
#### Consultation

- Description: these endpoints are related to consultation data. It allows accessing, creating, updating, and deleting data regarding consultations.

- Endpoints:
	-  `GET`  `{base_url}/consultations`
		desc: Getting all available consultation data from the db. It also allows pagination via query parameter. It also enable searching data by keyword via query parameter.
		available query param:
		-  `with_pagination`  `True/False`
		-  `skip`  `int`
		-  `limit`  `int`
		-  `search`  `string`

	-  `GET`  `{base_url}/consultations/{consultation_id}`
		desc: Getting consultation data from the db based on `consultation_id`.

	-  `POST`  `{base_url}/consultations`
		desc: Create new patient data and insert it into the db. Consultation date must be written in `year-month-date` format. Consultation creation will fail if any of doctor, patient, and doctor time slot data does not exist. Only consultation where today is at least `1 day prior` to consultation date can be created. Creation will also fail if the requested date does not match the time slot day or the time slot is `inactive`
		sample payload:
	
			{
				"date": "2020-12-01",
				"doctor_id": 1,
				"patient_id": 1,
				"time_slot_id": 1
			}

	-  `PUT`  `{base_url}/consultations/{consultation_id}/write-diagnosis`
desc: Update consultation diagnosis based on `consultation_id`. This process will fail if diagnosis already updated in the consultation data.
	sample payload:

			{
				"diagnosis": "Common cold",
				"note":  "Rest"
			}
			
	-  `DELETE`  `{base_url}/consultations/{consultation_id}`
		desc: Deleting consultation data based on `consultation_id`. Deletion process will fail if `diagnosis` already written in said consultation data.