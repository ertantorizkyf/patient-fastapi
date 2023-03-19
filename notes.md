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

- Description: these endpoints are related to medical speciality data. It allows accessing, creating, updating, and deleting data regarding specialities. Specialities data are needed to insert doctor data as the doctors needed `speciality_id` to be created.

- Endpoints:
	-  `GET`  `{base_url}/specialities`
		desc: Getting all available medical specilatity data from the db. It also allows pagination via query parameter. It also enable searching data by keyword via query parameter.
		available query param:
		-  `with_pagination`  `True/False`
		-  `skip`  `int`
		-  `limit`  `int`
		-  `search`  `string`

	-  `GET`  `{base_url}/specialities/{speciality_id}`
		desc: Getting speciality data from the db based on `speciality_id`.

	-  `POST`  `{base_url}/specialities`
		desc: Create new speciality data and insert it into the db.		sample payload:
	
			{
				"name": "General Practitioner"
			}
			
	-  `DELETE`  `{base_url}/specialities/{speciality_id}`
		desc: Deleting speciality data based on `speciality_id`. Deletion process will fail if `speciality_id` exists in doctor data.

  
#### Doctor

- TBU

  
#### Consultation

- TBU