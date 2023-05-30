# SIIM Hackathon CLI

SIIM Hackathon dataset CLI is a command-line tool that allows you to add new data to the dataset and modify existing DICOM tags to fit the SIIM Hackathon data format.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/siim-hackathon-cli.git
   ```
2. Navigate to the project directory:

   ```bash
   cd siim-hackathon-cli
   ```
3. Create a virtual environment (optional but recommended):

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
4. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```
## Usage
To use the SIIM Hackathon CLI, execute the following command:

```bash
siim-hackathon <command> [options]
```
Available commands:

- `modify_dicom_tags`: Modify existing DICOM data to fit the SIIM Hackathon data format.
- `dcm2fhir`:          Export dicom images into FHIR imaging resource (as json file) according to siim-hackathon data format.
### modify_dicom_tags Command
This command modifies DICOM tags in existing files to fit the SIIM Hackathon data format.

````bash
siim-hackathon modify_dicom_tags --input-directory <input_directory> --tag_modifier_request <tag_modifier_request> --output-directory <output_directory> [--validated-dicom]
````
Options
--input-directory, -i: Path to the input directory containing DICOM files.  
--tag_modifier_request, -req: Path to the DICOM tag request YAML file. [optional]  
--output-directory, -o: Path to the output directory to save modified DICOM files.   
--validated-dicom: Validate that the DICOM file is a valid DICOM (flag).[Not implemented yet]    
#### Tag Modifier Request YAML file
The tag modifier request YAML file is used to specify the DICOM tags to be modified. The file should be in the following format:
Look at ``default_tag_modifier_request.yaml`` for an example.
### dcm2fhir Command
This command converts DICOM images into FHIR imaging resource (as json file) according to siim-hackathon data format.

````bash
siim-hackathon dcm2fhir --input-directory <input_directory> --output-directory <output_directory>
````
Options   
--input-directory, -i: Path to the input directory containing DICOM files.    
--output-directory, -o: Path to the output directory to save FHIR imaging resource files.    



## Contributing
Contributions are welcome! If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License
This project is licensed under the MIT License.

# Roadmap

-[x] Convert dicom images into the SIIM DICOM format
-[x] Create a setup to install the CLI
-[x] Convert one DICOM study into FHIR imaging resource (as json file)
-[x] Create a basic dicom tag faker 
-[ ] Validate modified dicom images using pydicom validator
-[x] Handle several studies at once
-[ ] Create patient FHIR resource from DICOM image
-[ ] Run the service inside Docker container

