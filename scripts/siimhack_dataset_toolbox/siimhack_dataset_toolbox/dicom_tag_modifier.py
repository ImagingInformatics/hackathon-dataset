from datetime import datetime

from pydicom.dataset import Dataset
from pydicom.datadict import dictionary_VR
from faker import Faker

from siimhack_dataset_toolbox.dicom_vr_faker import DicomVRProvider

faker = Faker()
faker.add_provider(DicomVRProvider)


def modify_single_dicom_tag(dataset_handle: Dataset, tag: str, vr: str ,value=None):
    """Modify a DICOM tag value if tag already existing, otherwise create it.
    :param dataset_handle: Handle to the pydicom dataset
    :param tag: tag to add or modify
    :param value: tag's value
    :param vr: tag's value representation
    :return: dataset_handle
    """
    faker_kwargs = value.get("faker_kwargs", {})

    if vr == "AE":
        value = "SIIMHACK_AE"
    elif vr == "AS":
        patient_birth_date = datetime.strptime(dataset_handle.PatientBirthDate, '%Y%m%d')
        study_date = datetime.strptime(dataset_handle.StudyDate, '%Y%m%d')
        value = faker.dicom_age(study_date=study_date, patient_birth_date=patient_birth_date, **faker_kwargs)
    elif vr == "DA":
        value = faker.dicom_date(**faker_kwargs)
    elif vr == "UI":
        value = faker.dicom_uid(**faker_kwargs)
    elif vr == "SH":
        value = faker.dicom_sh(**faker_kwargs)



    if tag in dataset_handle:
        dataset_handle[tag].value = value
    else:
        assert vr is not None, "Value representation must be specified for new tags"
        dataset_handle.add_new(tag, vr, value)
    return dataset_handle


def modify_dicom_tags(dataset_handle: Dataset, tags: dict):
    """Modify dictionary of dicom tags
    :param dataset_handle: Handle to the pydicom dataset
    :param tags: dictionary of tags to add or modify
    :return: dataset_handle
    """
    for tag, value in tags.items():
        vr = dictionary_VR(tag)
        if not value: value = None
        dataset_handle = modify_single_dicom_tag(dataset_handle, tag, vr, value)
    return dataset_handle
