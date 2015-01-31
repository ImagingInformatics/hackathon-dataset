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

# Patient Narratives
##BreastDx-01-0003

##LIDC-IDRI-0132

##TCGA-17-Z058

##TCGA-50-5072

##TCGA-BA-4077

