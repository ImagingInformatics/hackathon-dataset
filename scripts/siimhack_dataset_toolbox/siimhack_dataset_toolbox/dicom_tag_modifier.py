from datetime import datetime

from dicom.tag import Tag
from pydicom.dataset import Dataset
from pydicom.datadict import dictionary_VR
from faker import Faker

from siimhack_dataset_toolbox.dicom_vr_faker import DicomVRProvider

faker = Faker()
faker.add_provider(DicomVRProvider)


def modify_single_dicom_tag(dataset_handle: Dataset, tag: str, vr: str, request: dict):
    """Modify a DICOM tag value if tag already existing, otherwise create it.
    :param dataset_handle: Handle to the pydicom dataset
    :param tag: tag to add or modify
    :param value: tag's value
    :param vr: tag's value representation
    :return: dataset_handle
    """
    faker_kwargs = request.get("faker_kwargs", {})
    # Use "tag" keyword to set faker condition based on dicom tag value.
    # Useful for date related tags
    # If tag don't exist, use default key
    for key, value in faker_kwargs.items():
        if isinstance(value, dict) and "tag" in value:
            faker_kwargs[key] = dataset_handle[value["tag"]].value
        elif isinstance(value, dict):
            faker_kwargs[key] = value.get("default", '')

    if vr == "AE":
        value = "SIIMHACK_AE"
    elif vr == "AS":
        value = faker.dicom_age(**faker_kwargs)
    elif vr == "DA":
        value = faker.dicom_date(**faker_kwargs)
    elif vr == "SH":
        value = faker.dicom_sh(**faker_kwargs)
    elif vr == "LO":
        value = faker.dicom_lo(**faker_kwargs)
    elif vr == "UI":
        value = faker.dicom_uid(**faker_kwargs)
    elif vr == "PN":
        value = faker.person_name(**faker_kwargs)
    else:
        raise ValueError(f"{vr} value generation not supported yet.")

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
    for tag, request in tags.items():
        vr = dictionary_VR(tag)
        if not request: request = {}
        dataset_handle = modify_single_dicom_tag(dataset_handle, tag, vr, request)
    return dataset_handle


if __name__ == '__main__':
    import pydicom
    import yaml

    dataset_handler = pydicom.dcmread("./IM-0026-0001.dcm")
    # read yaml
    with open("default_siim_hackathon_dataset_request.yaml", 'r') as f:
        tags = yaml.safe_load(f)
    dataset_handler = modify_dicom_tags(dataset_handler, tags)
    print(dataset_handler.PatientID)
    print(dataset_handler.PatientBirthDate)