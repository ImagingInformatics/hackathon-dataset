import string
from datetime import datetime
import random

from faker.providers import BaseProvider
from faker import Faker
from pydicom.uid import generate_uid


class DicomVRProvider(BaseProvider):
    """A provider that simulate several dicom VR."""

    def __init__(self, seed: int = 0):
        Faker.seed(seed)

    def person_name(self, firstname='', lastname='', gender: str = None):
        """Return a fake person name based on gender if provided, in the dicom format, e.g. Doe^John or Doe^Jane.
        :param firstname: (str) or None. Specify the firstname for a fixed value
        :param lastname: (str) or None. Specify the lastname for a fixed value
        :param gender: (M or F) or None. Specify the gender"""
        if firstname and lastname:
            return f"{lastname}^{firstname}"

        fake = Faker()
        gender = gender.upper()

        if firstname and not lastname:
            lastname = fake.last_name()
            return f"{lastname}^{firstname}"

        assert gender in {'M', 'F', None}
        if gender:
            firstname = fake.first_name_female if gender == 'F' else fake.first_name_male()
        else:
            firstname = fake.first_name()
        if not lastname:
            lastname = fake.last_name()
        return f"{lastname}^{firstname}"

    def dicom_time_entry(self, ):
        """The dicom time entry has a format of hhmmss.frac
        hh is in the range 00-23, mm in the range of 00-59, ss in the range of 00-60, and frac in the range of 0-999999.
        """
        fake = Faker()
        return fake.time(pattern="%H%M%S.") + (str(fake.random_int(min=0, max=999999))).zfill(6)

    def dicom_date(self, before: str = None, after: str = None):
        """The dicom date entry has a format of YYYYMMDD.
        :param before: (str) or None. Specify a date before the current date
        :param after: (str) or None. Specify a date after the current date (format -30y for example)
        """
        fake = Faker()
        if not before:
            before = datetime.now()
        if after:
            return fake.date_between(start_date=after, end_date=before).strftime("%Y%m%d")
        return fake.date(pattern="%Y%m%d", end_datetime=before)

    def dicom_age(self, study_date: str, patient_birth_date: str):
        if not patient_birth_date:
            patient_birth_date = self.dicom_date()
        birth_date = datetime.strptime(patient_birth_date, '%Y%m%d')
        current_date = datetime.strptime(study_date, '%Y%m%d')
        age = (current_date - birth_date).days / 365
        return f"{int(age)}Y"

    def dicom_sh(self,
                 length: int = 10,
                 only_digits: bool = True,
                 only_letters: bool = False):
        """Generate a random accession number."""
        if length > 64:
            raise ValueError("The maximum length of a Short String is 64 characters.")
        fake = Faker()
        if only_digits: return fake.random_number(digits=length)
        if only_letters: return fake.random_letters(length=length)
        letters_and_digits = string.ascii_letters + string.digits
        return ''.join(random.choice(letters_and_digits) for _ in range(length))

    def dicom_uid(self, org_root: str = ''):
        """Generate a valid dicom uid. If org_root is not provided, a random one will be generated."""
        return str(generate_uid(prefix=org_root)) if org_root else str(generate_uid())
