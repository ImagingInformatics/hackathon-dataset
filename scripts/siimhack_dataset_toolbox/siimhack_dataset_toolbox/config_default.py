siim_default_configuration = {
    'PatientName': {
        'faker_kwargs': {
            'firstname': '',  # provide a firstname. if not, one is generated
            'lastname': '',  # provide a lastname. if not, one is generated
            'gender': {
                'tag': 'PatientSex'  # provide a gender. if not, one is generated. Should be 'M' or 'F'
            }
        }
    },
    'StudyDate': {
        'faker_kwargs': {
            'default_value': {
                'tag': 'StudyDate'  # Keep the study date if already present
            },
            'before': '',  # provide a before date. if not, now is generated
            'after': '-5y'
        }
    },
    'PatientBirthDate': {
        'faker_kwargs': {
            'before': '-20y',  # provide a before date. if not, now is generated
            'after': '-80y'
        }
    },
    'PatientAge': {
        'faker_kwargs': {
            'patient_birth_date': {
                'tag': 'PatientBirthDate'
            },
            'study_date': {
                'tag': 'StudyDate'
            }
        }
    },
    'AccessionNumber': {
        'faker_kwargs': {
            'length': 10,
            'only_digits': True,
            'only_letters': False
        }
    },
    'PatientID': {
        'faker_kwargs': {
            'default_value': {
                'tag': 'PatientID'  # Provide an unique patient id
            }
        }
    }
}