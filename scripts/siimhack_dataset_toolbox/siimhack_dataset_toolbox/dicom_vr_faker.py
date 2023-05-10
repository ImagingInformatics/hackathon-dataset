import string
from datetime import datetime
import random
from typing import Any

from faker.providers import BaseProvider
from faker import Faker
from pydicom.uid import generate_uid


class DicomVRProvider(BaseProvider):
    """A provider that simulate several dicom VR."""

    def __init__(self, generator: Any, seed: int = 15):
        super().__init__(generator)
        Faker.seed(seed)
        self.fake = Faker()

    def person_name(self, firstname='', lastname='', gender: str = None):
        """Return a fake person name based on gender if provided, in the dicom format, e.g. Doe^John or Doe^Jane.
        :param firstname: (str) or None. Specify the firstname for a fixed value
        :param lastname: (str) or None. Specify the lastname for a fixed value
        :param gender: (M or F) or None. Specify the gender"""
        if firstname:
            if lastname:
                return f"{lastname}^{firstname}"

            lastname = self.fake.last_name()
            return f"{lastname}^{firstname}"

        gender = gender.upper() if gender else self.fake.random_element(['M', 'F'])
        firstname = self.fake.first_name_female() if gender == 'F' else self.fake.first_name_male()
        lastname = lastname or self.fake.last_name()
        return f"{lastname}^{firstname}"

    def dicom_time_entry(self, ):
        """The dicom time entry has a format of hhmmss.frac
        hh is in the range 00-23, mm in the range of 00-59, ss in the range of 00-60, and frac.
        """
        return self.fake.time(pattern="%H%M%S.") + "000000"

    def dicom_date(self, default_value: str = None, before: str = None, after: str = None):
        """The dicom date entry has a format of YYYYMMDD.
        :param before: (str) or None. Specify a date before the current date
        :param after: (str) or None. Specify a date after the current date (format -30y for example)
        """
        if default_value:
            return default_value
        if not before:
            before = datetime.now()
        return self.fake.date_between(start_date=after, end_date=before).strftime("%Y%m%d") \
            if after \
            else self.fake.date(pattern="%Y%m%d", end_datetime=before)

    def dicom_age(self, study_date: str, patient_birth_date: str):
        """Return the DICOM age in the format 'N[Y|M|W|D]'.
        :param study_date: (str) The date of the study in the format YYYYMMDD.
        :param patient_birth_date: (str) or None. The date of birth of the patient in the format YYYYMMDD.
        """

        birth_date = datetime.strptime(patient_birth_date, '%Y%m%d')
        study_date = datetime.strptime(study_date, '%Y%m%d')
        age_in_days = (study_date - birth_date).days
        if age_in_days < 30:
            return f"{age_in_days}D"
        elif age_in_days < 365:
            return f"{age_in_days // 30}M"
        else:
            return f"{age_in_days // 365}Y"

    def _dicom_s(self, default_value: str = None,
                 length: int = 10,
                 only_digits: bool = True,
                 only_letters: bool = False):
        """Generate a random accession number or the default provided value."""
        if default_value:
            return default_value
        if only_digits:
            return self.fake.random_number(digits=length)
        if only_letters:
            return self.fake.random_letters(length=length)
        letters_and_digits = string.ascii_letters + string.digits
        return ''.join(random.choice(letters_and_digits) for _ in range(length))

    def dicom_sh(self,
                 default_value: str = None,
                 length: int = 10,
                 only_digits: bool = True,
                 only_letters: bool = False):
        """Generate a random accession number or the default provided value."""
        if length > 64:
            raise ValueError("The maximum length of a Short String is 64 characters. Please use Long String for "
                             "longer values.")
        return self._dicom_s(default_value, length, only_digits, only_letters)

    def dicom_lo(self,
                 default_value: str = None,
                 length: int = 10,
                 only_digits: bool = True,
                 only_letters: bool = False):
        """Generate a random accession number or the default provided value."""
        return self._dicom_s(default_value, length, only_digits, only_letters)

    def dicom_uid(self, org_root: str = ''):
        """Generate a valid dicom uid. If org_root is not provided, a random one will be generated."""
        return str(generate_uid(prefix=org_root)) if org_root else str(generate_uid())
