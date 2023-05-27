import os
from datetime import datetime

import numpy as np
from dicom.tag import Tag
import pydicom
from pydicom.dataset import Dataset
from pydicom.datadict import dictionary_VR
from faker import Faker
from tqdm import tqdm

from siimhack_dataset_toolbox.dicom_vr_faker import DicomVRProvider


class DICOMTagModifier:
    """
    A class for modifying DICOM tags in a directory of DICOM files.

    Args:
        faker (Faker): An instance of the Faker class for generating fake DICOM tag values.
        input_directory (str): The path to the input directory containing the DICOM files.
        output_directory (str): The path to the output directory where modified DICOM files will be saved.
    """

    def __init__(self, input_directoy, output_directory, faker=None):
        if not faker:
            faker = Faker()
            faker.add_provider(DicomVRProvider)
        self.faker = faker
        self.patient_values = {}
        self.input_directory = os.path.abspath(input_directoy)
        self.output_directory = os.path.abspath(output_directory)

    def walk_directory(self):
        """
        Recursively walks through the input directory and yields DICOM file paths and corresponding output directories.

        Yields:
            tuple: A tuple containing the DICOM file path and the output directory path.
        """
        for root, dirs, files in os.walk(self.input_directory):
            if files:
                output_root = root.replace(self.input_directory, self.output_directory)
                for file in files:
                    dicom_file_path = os.path.join(root, file)
                    if pydicom.misc.is_dicom(dicom_file_path):
                        if not os.path.exists(output_root):
                            os.makedirs(output_root)
                        yield dicom_file_path, output_root

    def modify_dicom_tags(self, request: dict):
        """
        Modifies DICOM tags in the input directory using the provided request dictionary.

        Args:
            request (dict): A dictionary containing the tags to modify and their corresponding modification rules.
        """
        dicom_files = []
        output_roots = []
        for dicom_file, output_root in self.walk_directory():
            dicom_files.append(dicom_file)
            output_roots.append(output_root)

        for dicom_file, output_root in tqdm(zip(dicom_files, output_roots), total=len(dicom_files)):
            dataset_handle = pydicom.dcmread(dicom_file)
            dataset_handle = self._modify_tags_helper(dataset_handle, request)
            filename = os.path.basename(dicom_file)
            output_file = os.path.join(output_root, filename)
            dataset_handle.save_as(output_file)

    def get_single_dicom_tag(self, dataset_handle: Dataset, vr: str, request: dict):
        """
        Gets a DICOM tag value if the tag already exists, otherwise creates it.

        Args:
            dataset_handle (pydicom.dataset.Dataset): Handle to the pydicom dataset.
            vr (str): The DICOM tag's value representation.
            request (dict): The request dictionary containing the modification rules.

        Returns:
            any: The modified DICOM tag value.
        """
        faker_kwargs = request.get("faker_kwargs", {})
        # Use "tag" keyword to set faker condition based on dicom tag value.
        # Useful for date related tags
        # If tag don't exist, use default key
        for key, value in faker_kwargs.items():
            if isinstance(value, dict) and "tag" in value:
                faker_kwargs[key] = dataset_handle[value["tag"]].value
            elif key == "default_value":
                faker_kwargs[key] = faker_kwargs.get("default_value", '')

        if vr == "AE":
            value = "SIIMHACK_AE"
        elif vr == "AS":
            value = self.faker.dicom_age(**faker_kwargs)
        elif vr == "DA":
            value = self.faker.dicom_date(**faker_kwargs)
        elif vr == "SH":
            value = self.faker.dicom_sh(**faker_kwargs)
        elif vr == "LO":
            value = self.faker.dicom_lo(**faker_kwargs)
        elif vr == "UI":
            value = self.faker.dicom_uid(**faker_kwargs)
        elif vr == "PN":
            value = self.faker.person_name(**faker_kwargs)
        else:
            raise ValueError(f"{vr} value generation not supported yet.")
        return value

    def _modify_tags_helper(self, dataset, requests: dict):
        """
        Modifies DICOM tags in the dataset based on the provided requests.

        Args:
            dataset (pydicom.dataset.Dataset): The pydicom dataset to modify.
            requests (dict): A dictionary containing the tags to modify and their corresponding modification rules.

        Returns:
            pydicom.dataset.Dataset: The modified pydicom dataset.
        """
        patient_id = dataset.PatientID
        if patient_id not in self.patient_values:
            self.patient_values[patient_id] = {}

        for tag, request in requests.items():
            if tag not in self.patient_values[patient_id]:
                vr = dictionary_VR(tag)
                if not request: request = {}
                value = self.get_single_dicom_tag(dataset, vr, request)
                self.patient_values[patient_id][tag] = value
            if tag in dataset:
                dataset[tag].value = self.patient_values[patient_id][tag]
            else:
                dataset.add_new(tag, dictionary_VR(tag), self.patient_values[patient_id][tag])
                # doing it like this as we can modify the patient_id while using the original patient_id as entry key
        return dataset


if __name__ == "__main__":
    import pydicom
    import yaml

    faker = Faker()
    faker.add_provider(DicomVRProvider)
    with open("../default_siim_hackathon_dataset_request.yaml", 'r') as f:
        request = yaml.safe_load(f)
    dm = DICOMTagModifier(faker, "C:/Users/StephanHahn/Documents/perso/siim/hackathon-images/Sally SIIM", "./test")
    dm.modify_dicom_tags(request)
    # process_dicom_files("./", "./test", "default_siim_hackathon_dataset_request.yaml")
    # img = pydicom.dcmread("IM-0026-0001.dcm")
    # with open("default_siim_hackathon_dataset_request.yaml", 'r') as f:
    #     request = yaml.safe_load(f)
    # img = modify_dicom_tags(img, request)
