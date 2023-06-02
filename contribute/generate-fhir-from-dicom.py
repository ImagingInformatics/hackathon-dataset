import sys, os, requests, json, argparse, pydicom, pathlib

encounteredPatientIds = [] # List of encountered Patients IDs (to avoid duplication)
encounteredStudyUids = [] # List of encountered Studies UIDs (to avoid duplication)
encounteredSeriesUids = [] # List of encountered Series UIDs (to avoid duplication)

patientResources = [] # List of FHIR Patient resources
studyResources = [] # List of FHIR ImagingStudy resources
reportResources = [] # List of FHIR DiagnosticReport resources

fhirOutputDirName = 'generated-fhir-resources'


def dicomtToFhirDate(dicomDate : str):
    return dicomDate[0:4] + '-' + dicomDate[4:6] + '-' + dicomDate[6:8]


def dicomtToFhirInstant(dicomDate : str, dicomTime : str, timezone : str = "+00:00"):
    return dicomDate[0:4] + '-' + dicomDate[4:6] + '-' + dicomDate[6:8] + 'T' + dicomTime[0:2] + ':' + dicomTime[2:4] + ':' + dicomTime[4:6] + timezone



def processDicomFile(dcmFile :str , reportsFlag : bool):
    dicom = None
    try:
        dicom = pydicom.dcmread(dcmFile)
    except:
        print("Skipped over none-DICOM file:" + dcmFile, flush=True)
        return

    currentPath = str(pathlib.Path(__file__).parent.resolve())
    patient = json.load(open(currentPath + "/patient-template.txt",mode='r'))
    study = json.load(open(currentPath + "/imagingStudy-template.txt",mode='r'))

    # Update the Patient object
    pid = str(dicom.PatientID)
    names = str(dicom.PatientName).split('^')
    gender = str(dicom.PatientSex)
    dob = str(dicom.PatientBirthDate)
    acn = str(dicom.AccessionNumber)
    studyUid = str(dicom.StudyInstanceUID)
    seriesUid = str(dicom.SeriesInstanceUID)
    desc = str(dicom.StudyDescription)
    studyDate = str(dicom.StudyDate)
    studyTime = str(dicom.StudyTime)
    identifierPatient = "".join(names).lower() # E.g. siimravi
    identifierStudy = acn
    identifierSeries = seriesUid

    # If accesion number is empty, take the last chunk of the SUID
    if identifierStudy == '':
        parts = studyUid.split('.')
        identifierStudy = parts[len(parts) - 1] # HAPI likes the identifier to start with a character

    # HAPI does not like numeric identifiers
    if identifierPatient.isnumeric():
        identifierPatient = 'p' + identifierPatient
    if identifierStudy.isnumeric():
        identifierStudy = 'a' + identifierStudy

    patient['id'] = identifierPatient
    patient['identifier'][0]['value'] = pid
    patient['name'][0]['family'] = names[0]
    patient['name'][0]['given'][0] = names[1] if len(names) > 1 else names[0]

    # Translate DICOM sex to FHIR Gender
    if gender == 'F':
        patient['gender'] = 'female'
    elif gender == 'M' :
        patient['gender'] = 'male'
    elif gender == 'O':
        patient['gender'] = 'other'
    else:
        patient['gender'] = 'unknown'

    # Update the date format to match FHIR's
    if dob == '':
        del patient['birthDate']
    else:
        patient['birthDate'] = dicomtToFhirDate(dob)

    # In case study time is not filled out
    if studyTime is None or studyTime == '':
        studyTime = '000000'

    # Update the ImagingStudy object
    study['id'] = identifierStudy
    study['identifier'][0]['value'] = studyUid
    study['identifier'][1]['value'] = acn
    study['subject']['reference'] = 'Patient/' + identifierPatient
    study['description'] = desc
    study['started'] = dicomtToFhirDate(studyDate)


    # Update the DiagnosticReport object, if requested
    report = None
    if reportsFlag:
        report = json.load(open(currentPath + "/diagnosticReport-template.txt", mode='r'))
        report['id'] = identifierStudy
        report['issued'] = dicomtToFhirInstant(studyDate, studyTime)
        report['subject']['reference'] = 'Patient/' + identifierPatient
        report['identifier'][0]['value'] = acn
        report['effectiveDateTime'] = dicomtToFhirDate(studyDate)

    # Check if this patient/study/series were encountered before
    if identifierPatient not in encounteredPatientIds:
        encounteredPatientIds.append(identifierPatient)
        patientResources.append(patient)

    if identifierStudy not in encounteredStudyUids:
        encounteredStudyUids.append(identifierStudy)
        encounteredSeriesUids.append(identifierSeries)
        studyResources.append(study)
        if reportsFlag:
            reportResources.append(report)

    else: # Study has been seen before - increment instance and possible series counter
        for studyResource in studyResources:
            if studyResource['id'] == identifierStudy:
                studyResource['numberOfInstances'] += 1
                if identifierSeries not in encounteredSeriesUids:
                    studyResource['numberOfSeries'] += 1
                    encounteredSeriesUids.append(identifierSeries)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Traverse a list of DICOM files (nested within directories) and generated FHIR Patient, ImagingStudy and optionally DiagnosticReport resources based on the DICOM data. The FHIR resources are persisted to disk under the current directory.')
    parser.add_argument('-d', '--dicom', type=str, nargs='?', required=True, help="Path to the directory containting DICOM Data")
    parser.add_argument('-r', '--reports', type=bool, nargs='?', required=False, help="Whether or not to generate FHIR DiagnosticReports for each study (report text would be set to dummy text and must be updated by hand)")
    args = parser.parse_args()
    dicomCounter = 0
    patientCounter = 0
    studyCounter = 0
    reportCounter = 0

    # Ensure the output directory exists or gets created
    outputDir = os.path.join(os.path.curdir, fhirOutputDirName)
    if not os.path.exists(outputDir):
        os.mkdir(outputDir)

    # Loop through DICOM files
    for root, dirs, files in os.walk(args.dicom):
        for f in files:
            processDicomFile(os.path.join(root, f), args.reports)
            dicomCounter += 1
    print(f"Processed {dicomCounter} file(s)", flush=True)

    # Persist the FHIR resources
    for patient in patientResources:
        patientDir = os.path.join(outputDir, patient['name'][0]['family'].lower() + '_' + patient['name'][0]['given'][0].lower() + '-' + patient['id'].lower())
        # Create the directory if it doesn't exist
        if not os.path.exists(patientDir):
            os.mkdir(patientDir)

        # Write patient file
        patientFile = open(os.path.join(patientDir, 'patient.' + patient['id'].lower() + '.json'), "w")
        patientFile.write(json.dumps(patient, indent=2))
        patientFile.close()
        patientCounter += 1

        # Write study files
        for study in studyResources:
            # Ensure the study belongs to this patient
            if study['subject']['reference'] != 'Patient/' + patient['id']:
                continue

            # Write study file
            studyFile = open(os.path.join(patientDir, 'imaging_study.' + study['identifier'][0]['value']  + '.json'), "w")
            studyFile.write(json.dumps(study, indent=2))
            studyFile.close()
            studyCounter += 1

        # If reports were not requested, then skip
        if not args.reports:
            continue

        for report in reportResources:
            # Ensure the report belongs to this patient
            if report['subject']['reference'] != 'Patient/' + patient['id']:
                continue

            # Write report file
            reportFile = open(os.path.join(patientDir, 'diagnostic_report.' + report['identifier'][0]['value']  + '.json'), "w")
            reportFile.write(json.dumps(report, indent=2))
            reportFile.close()
            reportCounter += 1

    print(f"Wrote {patientCounter} Patient resources, {studyCounter} ImagingStudy resources and , {reportCounter} DiagnosticReport resources", flush=True)