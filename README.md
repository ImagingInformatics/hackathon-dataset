# siim-dataset
Collection of FHIR JSON objects representing fictious patient vignettes for use in our hackathon environment.

# What?
The [Society for Imaging Informatics in Medicine (SIIM)](http://www.siim.org/) is supporting the new DICOMWEB and FHIR standards by creating opportunities for it's members to interact with these systems at the annual meeting, and throughout the year through it's Hackathon/HackPack projects.

We're using images from [The Cancer Imaging Archive (TCIA)](http://www.cancerimagingarchive.net) and creating fictious but believable narratives that illustrate concepts common in imaging.

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

---------------------------------------

DIAGNOSTIC BILATERAL 4/12/2008

Clinical History:  59 year-old female with history of left invasive ductal carcinoma (age 55) status post lumpectomy.

Technique: Bilateral CC and MLO, Left spot compression LMLO views were obtained

Findings:

LEFT BREAST: There are scattered fibroglandular densities. There are expected lumpectomy changes in the upper outer quadrant with surgical clips in place.  Skin thickening is consistent with post radiation changes. No concerning masses, architectural distortions, or suspicious calcifications are identified.

RIGHT BREAST: There are scattered fibroglandular densities. No concerning masses, architectural distortions, or suspicious calcifications are identified.

Impression:

LEFT BREAST: Expected lumpectomy changes. Benign. BI-RADS 2 - Recommend routine screening in 1 year.

RIGHT BREAST: Negative. BI-RADS 1 - Recommend routine screening in 1 year.

OVERALL BI-RADS 2 (Benign)

---------------------------------------
Bilateral Breast MRI 04/19/2008

Clinical History:  59 year-old female with history of left invasive ductal carcinoma (age 55) status post lumpectomy. High-risk screening MRI exam.

Technique: Bilateral axial imaging of the breasts was obtained including T1, STIR, T1FS, and sequential T1FS+C. Digital subtraction and dynamic contrast curve analysis was performed on a separate workstation.

Findings:

LEFT BREAST: There is minimal benign background enhancement. There are expected post surgical changes in the upper outer breast. Multiple signal voids represent surgical clips in place.  Skin thickening is consistent with post radiation change. There is no abnormal enhancement to indicate residual or recurrent disease.  There are no morphologically abnormal axillary lymph nodes.

RIGHT BREAST: There is minimal benign background enhancement. There is no abnormal enhancement or lymphadenopathy.

Impression:

LEFT BREAST: Expected post treatment changes. Benign. BI-RADS 2. Recommend routine screening mammography in 1 year.

RIGHT BREAST: Negative. BI-RADS 1. Recommend routine screening mammography in 1 year.

OVERALL BI-RADS 2 (Benign)

---------------------------------------

Full Field Digital Left Diagnostic Mammogram 4/22/2008

Clinical History:  59 year-old female with history of left invasive ductal carcinoma (age 55) status post lumpectomy.

Technique: LML, L XCCL

Findings:

LEFT BREAST: There are scattered fibroglandular densities. There are expected lumpectomy changes in the upper outer quadrant with surgical clips in place.  Skin thickening is consistent with post radiation changes. No concerning masses, architectural distortions, or suspicious calcifications are identified.

Impression:

LEFT BREAST: Expected changes status post lumpectomy and radiation. Benign. BI-RADS 2 - Recommend routine screening in 1 year.

---------------------------------------
05/24/2008
Surgical Specimen Radiograph

Clinical History:  Unknown

Technique: Single surgical specimen radiograph

Findings: The surgical specimen contains an intact wire and surgical clip.  No masses or calcifications are identified.

Impression:

Specimen radiograph with intact wire and surgical clip.


###LIDC-IDRI-0132


###TCGA-17-Z058
HPI: 60 yo male with history of lung adenocarcinoma. 



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

Chest wall: No involvement.

Airway: Compression of the lingula

Vessels: Mass surrounds and nearly occludes the left inferior pulmonary artery.

Nerves: No involvement.

Regional extent
Lymph nodes: AP window, and right hilar adenopathy.

Distant metastases (chest and upper abdomen): None.

Other findings
Other findings: None. 

Impression
Left hilar mass concerning for malignancy.

---------------------------------------
PET Oncologic Study 4/22/1986

Duration of fast prior to injection: 6 hours

Blood glucose prior to injection: 85 mg/dl

Scan region: Brain, Neck, Chest, Abdomen

Radiopharmaceutical: F-18 FDG 10 mCi IV

Calibration time: 4/22/1986 10:30 AM

Administration time: 4/22/1986 10:32 AM

Injection site: left antecubital fossa

Post-injection imaging delay: 60 minutes

Attenuation correction: Rod source transmission scan.

Clinical information
60 yo male with left hilar mass, evaluate for metastatic disease

Comparison
Chest CT scan 3/30/1986

Findings
Hypermetabolic foci:
5.0 cm hypermetabolic left hilar mass on image 162 with a maximum SUV of 3.2.
1.8 x 1.2 cm hypermetabolic AP window lymph node on image 132 maximum SUV of 2.7
There is spurious activity in the neck musculature.  No contralateral hypermetabolic lesions are appreciated.

The right hilar adenopathy suspected on the prior CT scan is not seen.

Other findings:
The visualized brain parenchyma is unremarkable.  The soft tissues of the neck are unremarkable. The thyroid gland is unremarkable.  No axillary adenopathy.  No focal infiltrate.  No pneumothorax.  There a tiny left pleural effusion vs. pleural thickening.  This is not FDG avid.  The heart size is normal.  No pericardial effusion.

Lack of IV contrast mildly limits evaluation of the organs in the abdomen and pelvis. The liver is unremarkable without focal lesion.  The adrenals are normal.  The pancreas, spleen, and kidneys are unreamarkable.

Atherosclerotic calcification is seen throughout the aorta.  No abnormally dilated bowel.  No suspicious retroperitoneal or mesenteric adenopathy.

There are no suspicious bony lesions.

Impression
1. Findings again compatible with left hilar malignancy with a left AP window lymph node. There is no evidence of contralateral disease.

EORTC Response Criteria: N/A - Baseline

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

---------------------------------------

#### CT Chest, abdomen and pelvis 9/28/1986

Clinical indication
History of lung adenocarcinoma, followup.

Comparison
Multiple prior CTs, the most recent from 5/31/1986

Technique
Multidetector axial CT of the chest, abdomen and pelvis was performed after the administration of intravenous contrast in the portal venous phase.

Findings

Thorax:
The thyroid and thoracic inlet are normal. There are no enlarged axillary lymph nodes. There has been interval development of an enlarged lymph node conglomerate mass within the posterior mediastinum just anterior to the descending aorta, measuring 2.8 x 4.2 cm in axial dimension (series 5, image 36). This mass anteriorly displaces and mildly narrows the left main pulmonary artery. There is no clear evidence of vascular invasion. There is stable right hilar adenopathy. A new markedly enlarged precardial lymph node is also now seen, measuring 3.3 x 1.7 cm (series 5, image 42).

There is stable severe emphysema. A 4 mm left apical nodule (series 5, image 6) appears stable. Surgical changes from prior left lower lobectomy are evident with associated pleural thickening. A small left lateral rim enhancing pleural collection is suspicious for infection.

No suspicious osseous lesions. The visualized soft tissues are unremarkable.

Abdomen:
Punctate calcifications noted in the right hepatic lobe. Liver otherwise unremarkable. Gallbladder, pancrease, speen, and adrenal glands are normal. Bilateral renal cysts are noted. The kidneys are otherwise unremarkable with normal enhancement.

An enlarged gastrosplenic node is noted, measuring 1.3 cm in short axis dimension (series 6, image 13). The visualized bowel is within normal limits.

Impression
1. Post surgical changes from left lower lobectomy.

2. Development of posterior mediastinal and precardial lymphadenopathy concerning for disease progression. An enlarged gastrosplenic node is nonspecific and appears grossly stable compared to CT from 4/22/1986 given differences in technique.

3. Small rim enhancing left pleural fluid collection concerning for infection.



###TCGA-50-5072

###TCGA-BA-4077

