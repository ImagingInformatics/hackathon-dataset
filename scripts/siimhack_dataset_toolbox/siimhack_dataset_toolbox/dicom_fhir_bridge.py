import os
from datetime import datetime

import pydicom
from typing import Dict, List

from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding
from fhir.resources.endpoint import Endpoint
from fhir.resources.identifier import Identifier
from fhir.resources.imagingstudy import ImagingStudy, ImagingStudySeries, ImagingStudySeriesInstance
from dataclasses import dataclass

from fhir.resources.narrative import Narrative
from fhir.resources.reference import Reference
from tqdm import tqdm


class DICOMStudy:
    def __init__(self, study_id: str,
                 accession_number: str,
                 study_description: str,
                 study_date: str,
                 patient_name:str,
                 modality: str):
        """
        Represents a DICOM study.

        Args:
            study_id: The study ID.
        """
        self.study_id = study_id
        self.accession_number = accession_number
        self.series = {}
        self.num_series = 0
        self.num_instances = 0
        self.study_description = study_description
        self.study_date = study_date
        if '^' in patient_name:
            patient_name = patient_name.replace('^', '')
        self.patient_name = patient_name.lower()
        self.modality = modality

    def add_instance(self, series_id: str, file_path: str):
        """
        Adds a DICOM instance to the study.

        Args:
            series_id: The series ID of the instance.
            file_path: The file path of the instance.
        """
        if series_id not in self.series:
            self.series[series_id] = []
            self.num_series += 1

        self.series[series_id].append(file_path)
        self.num_instances += 1


class DICOMStudySplitter:
    def __init__(self):
        self.studies = {}

    def split_dicom_by_study(self, file_paths: List[str]) -> Dict[str, Dict[str, int]]:
        """
        Split a list of DICOM file paths by imaging study.

        Args:
            file_paths: A list of file paths of DICOM instances.

        Returns:
            A dictionary where the keys are study IDs, and the values are dictionaries
            containing the file paths of each instance in the study, the number of series
            in the study, and the number of instances in the study.
        """
        for file_path in file_paths:
            ds = pydicom.dcmread(file_path)
            study_id = ds.StudyInstanceUID
            series_id = ds.SeriesInstanceUID
            accession_number = ds.AccessionNumber
            study_description = ds.StudyDescription
            study_date = ds.StudyDate
            patient_name = str(ds.PatientName)
            modality = str(ds.Modality)

            if study_id not in self.studies:
                self.studies[study_id] = DICOMStudy(study_id,
                                                    accession_number,
                                                    study_description,
                                                    study_date,
                                                    patient_name,
                                                    modality)

            study = self.studies[study_id]
            study.add_instance(series_id, file_path)

        return {
            study_id: {
                'accession_number': study.accession_number,
                'study_description': study.study_description,
                'series': study.series,
                'modality' : study.modality,
                'num_series': study.num_series,
                'num_instances': study.num_instances,
                'study_date': study.study_date,
                'patient_name': study.patient_name
            }
            for study_id, study in self.studies.items()
        }


class ImagingStudyCreator:
    def create_imaging_studies(self, dicom_studies: Dict) -> List[ImagingStudy]:
        """
        Create ImagingStudy resources from a list of DicomStudy objects.

        Args:
            dicom_studies: List of DicomStudy objects.

        Returns:
            List of ImagingStudy resources.
        """
        imaging_studies = []

        for dicom_study_id,dicom_study  in tqdm(dicom_studies.items()):
            imaging_study = self.create_imaging_study(dicom_study_id,dicom_study)
            imaging_studies.append(imaging_study)

        return imaging_studies

    def create_imaging_study(self,dicom_study_id:str, dicom_study: DICOMStudy) -> ImagingStudy:
        """
        Create an ImagingStudy resource from a DicomStudy object.

        Args:
            dicom_study: DicomStudy object.

        Returns:
            ImagingStudy resource.
        """
        imaging_study = ImagingStudy()
        imaging_study.id = dicom_study["accession_number"]
        imaging_study.numberOfSeries = dicom_study['num_series']
        imaging_study.numberOfInstances = dicom_study['num_instances']

        imaging_study.text = Narrative()
        imaging_study.text.status = 'generated'
        imaging_study.text.div = f"<div xmlns=\"http://www.w3.org/1999/xhtml\">{dicom_study['study_description']}</div>"

        endpoint = Endpoint()
        endpoint.reference = "Endpoint/siim-dicomweb"
        # Initialize the imaging_study.endpoint as an empty list if it's None
        if imaging_study.endpoint is None:
            imaging_study.endpoint = []
        imaging_study.endpoint.append(endpoint)

        imaging_study.started = datetime.strptime(dicom_study['study_date'], "%Y%m%d").date().isoformat()

        if imaging_study.identifier is None:
            imaging_study.identifier = []

        identifier_urn = Identifier()
        identifier_urn.system = "urn:dicom:uid"
        identifier_urn.value = f"urn:oid:{dicom_study_id}"
        imaging_study.identifier.append(identifier_urn)

        identifier_accession = Identifier()
        identifier_accession.use = "usual"
        identifier_accession.type = CodeableConcept()
        identifier_accession.type.coding = []
        acsn_coding = Coding()
        acsn_coding.system = "http://terminology.hl7.org/CodeSystem/v2-0203"
        acsn_coding.code = "ACSN"
        identifier_accession.type.coding.append(acsn_coding)
        identifier_accession.value = dicom_study['accession_number']
        assigner = Reference()
        assigner.reference = "Organization/siim"
        identifier_accession.assigner = assigner
        imaging_study.identifier.append(identifier_accession)

        subject_reference = Reference()
        subject_reference.reference = f"Patient/{dicom_study['patient_name']}"
        imaging_study.subject = subject_reference
        imaging_study.description = dicom_study['study_description']

        series_creator = ImagingStudySeriesCreator()
        series_list = series_creator.create_series(dicom_study['series'],)
        imaging_study.series = series_list

        return imaging_study


class ImagingStudySeriesCreator:
    def create_series(self, series_dict: Dict[str, str]) -> List[ImagingStudySeries]:
        """
        Create ImagingStudySeries resources from a dictionary of series ID to DICOM file path.

        Args:
            series_dict: Dictionary of series ID to DICOM file path.

        Returns:
            List of ImagingStudySeries resources.
        """
        series_list = []

        for series_id, dicom_file_path in series_dict.items():
            series = self.create_series_instance(series_id, dicom_file_path)
            series_list.append(series)

        return series_list

    def create_series_instance(self, series_id: str, dicom_file_path: list) -> ImagingStudySeries:
        """
        Create an ImagingStudySeries resource from series ID and DICOM file path.

        Args:
            series_id: Series ID.
            dicom_file_path: DICOM file path.

        Returns:
            ImagingStudySeries resource.
        """
        ds_serie = pydicom.dcmread(dicom_file_path[0])
        series = ImagingStudySeries()
        series.uid = f"urn:oid:{ds_serie.SeriesInstanceUID}"

        modality_coding = Coding()
        modality_coding.system = "http://dicom.nema.org/resources/ontology/DCM"
        modality_coding.code = ds_serie.Modality
        series.modality = modality_coding

        series.description = ds_serie.SeriesDescription
        series.numberOfInstances = len(dicom_file_path)
        series.started = datetime.strptime(ds_serie.SeriesDate, "%Y%m%d").date().isoformat()

        instance_creator = ImagingStudyInstanceCreator()
        instances_list = instance_creator.create_instances(dicom_file_path)
        series.instance = instances_list

        return series


class ImagingStudyInstanceCreator:
    def create_instances(self, dicom_files:list) -> List[ImagingStudySeriesInstance]:
        """
        Create ImagingStudyInstance resources for a given series ID.

        Args:
            series_id: Series ID.

        Returns:
            List of ImagingStudyInstance resources.
        """
        instance_list = []
        for dicom_file in dicom_files:
            instance = self.create_instance(dicom_file)
            instance_list.append(instance)
        return instance_list
    def create_instance(self, dicom_file):
        ds_instance = pydicom.dcmread(dicom_file)
        instance = ImagingStudySeriesInstance()
        instance.uid = ds_instance.SOPInstanceUID
        instance.sopClass = ds_instance.SOPClassUID
        instance.number = ds_instance.InstanceNumber

        return instance


if __name__ == '__main__':
    def walk_directory(input_directory: str, output_directory: str):
        """
        Recursively walks through the input directory and yields DICOM file paths and corresponding output directories.

        Yields:
            tuple: A tuple containing the DICOM file path and the output directory path.
        """
        for root, dirs, files in os.walk(input_directory):
            if files:
                output_root = root.replace(input_directory, output_directory)
                for file in files:
                    dicom_file_path = os.path.join(root, file)
                    if pydicom.misc.is_dicom(dicom_file_path):
                        if not os.path.exists(output_root):
                            os.makedirs(output_root)
                        yield dicom_file_path, output_root
    input_directory = "C:/Users/StephanHahn/Documents/perso/siim/hackathon-images/Andy SIIM"
    output_directory = "./datasample/test"
    files = [file[0] for file in walk_directory(input_directory, output_directory)]
    dicom_study_splitter = DICOMStudySplitter()
    splitted = dicom_study_splitter.split_dicom_by_study(files)

    imaging_study_creator = ImagingStudyCreator()
    imaging_studies = imaging_study_creator.create_imaging_studies(splitted)
    print(imaging_studies)