import json
import logging
import os

import requests
import yaml

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# The HAPI FHIR server requires dependent objects to be loaded first
# TODO Upgrade the script so that dependencies can be resolved in a
# more automated, elegant fashion (reference detection) vs. this crude way
load_order = [
    "ValueSet",
    "Device",
    "Organization",
    "StructureDefinition",
    "Medication",
    "Practitioner",
    "PractitionerRole",
    "Patient",
    "AllergyIntolerance",
    "AdverseReaction",
    "Alert",
    "MedicationRequest",
    "MedicationDispense",
    "MedicationAdministration",
    "ImagingReference",
    "Observation",
    "Order",
    "OrderResponse",
    "Procedure",
    "Endpoint",
    "ImagingStudy",
    "DiagnosticReport",
    "Specimen",
    "Condition",
    "DocumentReference",
    "ImagingSelection"
]

if len(os.sys.argv) < 3:
    raise ValueError("usage:\n\npython upload.py server_config.yml path_for_recursion")

config_file = os.sys.argv[1]

if not os.path.exists(config_file):
    raise FileNotFoundError("Please specify a valid yml config file")
else:
    with open(config_file, "r") as file:
        server = yaml.safe_load(file)

# Test a basic GET against the FHIR server
try:
    result = requests.get(
        server["url"] + "Patient",
        headers={"apikey": server["apikey"]},
        params={"_format": server["format"]},
    )
    result.raise_for_status()
except requests.exceptions.RequestException as err:
    log.error(err)
    raise SystemExit(err)

fhir = {}

for root, dirs, files in os.walk(os.sys.argv[2]):
    for file in files:
        if file.endswith(".json"):
            data_path = os.path.join(root, file)
            try:
                log.info("Loading: {}".format(data_path))

                with open(data_path, "r") as data_file:
                    resource = json.load(data_file)

                resource_type = resource.get("resourceType", None)
                resource_id = resource.get("id", None)
                
                if resource_type is None:
                    log.error(
                        "Error reading {} - has no resourceType".format(
                            data_path
                        )
                    )
                    continue

                if resource_id is None:
                    log.error(
                        "Error reading {}, make sure an ID is specified in the header comment".format(
                            data_path
                        )
                    )
                    # raise ValueError

                fhir.setdefault(resource_type, []).append(resource)
            except Exception as e:
                log.error(f"Failed to load FHIR resource at {data_path} due to {e}")

# Make sure we have load_order for all of our resource types
missing_keys = set(fhir.keys()) - set(load_order)

if missing_keys:
    log.error("Resource Types missing from load order: {}".format(missing_keys))
    raise ValueError

for resource_type in load_order:
    if resource_type in fhir:
        for resource in fhir[resource_type]:
            resource_id = resource["id"]

            if resource_id is None:
                log.error(
                    "Error reading {}, make sure an ID is specified in the header comment".format(
                        resource
                    )
                )
                raise ValueError

            if resource_id == "random":
                url = server["url"] + resource_type
                try:
                    log.info("POST - {}".format(url))
                    result = requests.post(
                        url,
                        json=resource,
                        headers={
                            "Content-Type": server["format"] + "+fhir",
                            "apikey": server["apikey"],
                        },
                        params={"_format": server["format"]},
                    )
                    result.raise_for_status()
                except requests.exceptions.RequestException as e:
                    log.error(f"Failed to load {url} due to {e.response.text}")

            else:

                url = server["url"] + resource_type + "/" + resource_id
                try:
                    log.info("PUT - {}".format(url))
                    result = requests.put(
                        url,
                        json=resource,
                        headers={
                            "Content-Type": server["format"] + "+fhir",
                            "apikey": server["apikey"],
                        },
                        params={"_format": server["format"]},
                    )
                    result.raise_for_status()
                except requests.exceptions.RequestException as e:
                    log.error(f"Failed to load {url} due to {e.response.text}")

            result_json = result.json()
            # log.info("Submission Status: {}".format(result_json["issue"][0]["diagnostics"]))
