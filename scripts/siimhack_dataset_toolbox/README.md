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
### modify_dicom_tags Command
This command modifies DICOM tags in existing files to fit the SIIM Hackathon data format.

````bash
siim-hackathon modify_dicom_tags --input-directory <input_directory> --tag_modifier_request <tag_modifier_request> --output-directory <output_directory> [--validated-dicom]
````
Options
--input-directory, -i: Path to the input directory containing DICOM files.
--tag_modifier_request, -req: Path to the DICOM tag request YAML file.
--output-directory, -o: Path to the output directory to save modified DICOM files.
--validated-dicom: Validate that the DICOM file is a valid DICOM (flag).


## Contributing
Contributions are welcome! If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License
This project is licensed under the MIT License.

# Roadmap

-[x] Convert dicom images into the SIIM DICOM format
-[x] Create a setup to install the CLI
-[ ] Convert one DICOM study into FHIR imaging resource (as json file)
-[x] Create a basic dicom tag faker 
-[ ] Validate modified dicom images using pydicom validator
-[ ] Handle several studies at once
-[ ] Create patient FHIR resource from DICOM image
-[ ] Run the service inside Docker container
-[ ] Change configuration using CLI

