# siim-dataset
Collection of FHIR JSON objects representing fictious patient vignettes for use in our hackathon environment.

# What?
The [Society for Imaging Informatics in Medicine (SIIM)]http://www.siim.org/ is supporting the new DICOMWEB and FHIR standards by creating opportunities for it's members to interact with these systems at the annual meeting, and throughout the year through it's Hackathon/HackPack projects.

We're using images from [The Cancer Imaging Archive (TCIA)]http://www.cancerimagingarchive.net and creating fictious but believable narratives that illustrate concepts common in imaging.

This project will contain FHIR JSON objects surrounding these patient narratives.

# Why?
During our first hackathon, we realized that in order to have a successful hackathon across multiple platforms, we need to have a cohesive, rich dataset that will allow people to build interesting applications. 

# Organization
In the top level directory there are directories for resources that cross patients (Medications, Practitioner, Organizations)

Also within the top level directory are a set of sub-folders for each patient.  This skeleton contains a set of top-level directories that correspond with the FHIR Resources: http://www.hl7.org/implement/standards/fhir/resourcelist.html.  Within these sub-folders are json FHIR documents.

Each FHIR document should have a commented header that looks like this:
    // filename
    // id: random

If set to something other than random, this will be used to create the FHIR resource.

This is not meant to be an exhaustive collection, the types are chosen based on relevance to imaging patients.

# Uploading to a FHIR server
    cp fhir_server.yml.dist fhir_server.yml

Edit fhir_server.yml to fit your needs.

Install dependencies: ruby, bundler

Run Bundler to install needed gems
    bundle install

Run the script to upload all of the resources in the folders
    ruby update.rb

# Process to contribute
- Fork this repo
- Make your changes/improvements
- Send a pull request


# Patient Narratives
###BreastDx-01-0003
58 yo female DOB: 04/12/1950

HPI: Had a palpable left breast mass discovered on self-breast exam.  Patient was initially seen for diagnostic mammogram on 4/12/2008.  Patient had a lumpectomy on 5/24/2008.

PMHx: Hypothyroidism

Allergies: NKDA

Medications: levothyroxine sodium 50mcg once daily 

Lab/Radiology
4/12/2008 
Diagnostic mammogram revealed a mass with microcalcification in the outer portion of the left breast.  
BI-RADS Final Assessment Category IV: Suspicious for Malignancy.

---------------------------------------
04/19/2008
Bilateral breast MRI was also performed which demonstrated..........

---------------------------------------
4/22/2008
Left Diagnostic Mammogram demonstrates..........

---------------------------------------
05/24/2008
Specimen radiograph demonstrates.........

---------------------------------------
Pathology
5/24/2008
Invasive ductal carcinoma





###LIDC-IDRI-0132


###TCGA-17-Z058
HPI: 60 yo male with history of lung adenocarcinoma.  Pt has 8 CT scans of Abd/Pelvis.

####Imaging Exams
CT Onco Lung Mass 3/30/1986

Clinical information
60 yo male with left hilar mass.

Comparison
None.

Findings
Lung mass
Size: 5.3 x 4.0 x 4.0 cm

Location: left hilar region

Shape: Smoothly marginated

Internal consistency: homogenous, hypodense to surrounding muscle.

Local extent
Pleural surface: Left lower lobe metastasis

Chest wall: [No involvement.]

Airway: Compression of the lingula

Vessels: Mass surrounds and nearly occludes the left inferior pulmonary artery.

Nerves: [No involvement.]

Regional extent
Lymph nodes: AP window, and right hilar adenopathy.

Distant metastases (chest and upper abdomen): [None. ]

Other findings
Other findings [None. ]

Impression
Left hilar mass, compatible with adenocarcinoma.

---------------------------------------
PET Oncologic Study 4/22/1986
Duration of fast prior to injection: [      ]

Blood glucose prior to injection: [      ] mg/dl

Scan region: [      ]

Radiopharmaceutical: [F-18 FDG] [      ] mCi IV

Calibration time: [<date>] [<time>]

Administration time: [<date>] [<time>]

Injection site: [      ]

Post-injection imaging delay: [      ] minutes

Attenuation correction: [Rod source transmission scan. ]

Clinical information
[      ]

Comparison
[None. ]

Findings
Hypermetabolic foci: [None. ]

Other findings: [None.]

Impression
[      ]

EORTC Response Criteria: [Complete Metabolic Response. MaxSUV < 2.5 or equivalent to background | Partial Metabolic Response. Decrease in MaxSUV >= 25% | Progressive Metabolic Disease. Increase in MaxSUV > 25% | Stable Metabolic Disease. Change in MaxSUV < 25%]


---------------------------------------
SIIM Diagnostic Lab
Leesburg, VA
Tel: (555) 555-5555 Fax: (812) 353-5445

Surgical Pathology Report

Patient Name: TCGA-17-Z058. Accession #: XXX66-4444 Med. Rec. #: TCGA-17-Z058
Taken: 4/25/1986 Encounter #: 000111111111 Received: 4/25/1986 Gender: M
Reported: 4/26/1986 16:50 DOB: (Age: 60) Submitting Physician: REFERRING, MD
Additional Physician(s):
Location: ENDOSCOPY BL 

Pre-Operative Diagnosis:
Lingular lung mass

Post-Operative Diagnosis:
Same

Specimen Received:
Lingular lung bxs

Final Pathologic Diagnosis:
Lingula, lung, transbronchial biopsies:
Adenocarcinoma (see note)

The examination of this case material and the preparation of this report were
performed by the staff pathologist.
Electronically Signed by Joe Pathologist, M.D. 

Signing Location:
SIIM Laboratory Services,
Leesburg, VA

Gross Description:
Submitted in formalin as "left upper lobe-lung biopsies" are multiple fragments of light tan tissue each measuring up to 0.5 cm in greatest dimension. The entire specimen is submitted in a single cassette.

Microscopic Description:
Sections of bronchial mucosa demonstrate infiltration by poorly differentiated malignant cells which form cords and some, and somewhat pale cytoplasm. Some cells have a suggestion of signet ring cell morphology. No keratinization is evident. 

NOTE: This is a fictious report that was created to match the TCIA images.  This is NOT the actual report for this patient.

END OF REPORT



###TCGA-50-5072

###TCGA-BA-4077

