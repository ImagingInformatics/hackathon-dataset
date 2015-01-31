# siim-dataset
Collection of FHIR JSON objects representing fictious patient vignettes for use in our hackathon environment.

# What?
The [Society for Imaging Informatics in Medicine (SIIM)]http://www.siim.org/ is supporting the new DICOMWEB and FHIR standards by creating opportunities for it's members to interact with these systems at the annual meeting, and throughout the year through it's Hackathon/HackPack projects.

We're using images from [The Cancer Imaging Archive (TCIA)]http://www.cancerimagingarchive.net and creating fictious but believable narratives that illustrate concepts common in imaging.

This project will contain FHIR JSON objects surrounding these patient narratives.

# Why?
During our first hackathon, we realized that in order to have a successful hackathon across multiple platforms, we need to have a cohesive, rich dataset that will allow people to build interesting applications. 

# Organization
Each patient should be contained in it's own directory.

This skeleton contains a set of top-level directories that correspond with the FHIR Resources: http://www.hl7.org/implement/standards/fhir/resourcelist.html

This should make it easier for end users to load the information that they want without having to load everything.  

Each patient should have their own directory tree, so that it's easy to keep resources organized.

This is not meant to be an exhaustive collection, the types are chosen based on relevance to imaging patients.

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
Diagnostic mammogram revealed a mass with microcalcification in the outer portion of the left breast.  BI-RADS Final Assessment Category IV: Suspicious for Malignancy.

04/19/2008
Bilateral breast MRI was also performed which demonstrated..........

4/22/2008
Left Diagnostic Mammogram demonstrates..........

05/24/2008
Specimen radiograph demonstrates.........

Pathology
5/24/2008
Invasive ductal carcinoma


###LIDC-IDRI-0132

###TCGA-17-Z058
HPI: 60 yo male with history of lung adenocarcinoma.  Pt has 8 CT scans of Abd/Pelvis.

###TCGA-50-5072

###TCGA-BA-4077

