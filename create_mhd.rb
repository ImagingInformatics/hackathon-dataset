# create_mhd.rb
# This script reads all of the JSON objects contained in the children of the execution directory

require 'bundler'
require 'yaml'
require 'logger'
require 'erb'
require 'date'
require 'fileutils'

log = Logger.new(STDOUT)
log.level = Logger::DEBUG

Bundler::require

def generate_id
	# Generates a 16 digit random number
	Random.new.random_number(9999999999999999)
end

if ARGV.length < 1
	raise "usage:\n\nruby create_mhd.rb path_for_patient\n\nnote: only a single patient is currently supported"
end

if !File.directory?(ARGV[0])
	raise "input requires a directory to iterate over"
end

# IHE XDS classCode Value Set
report_class_code = {}
report_class_code["system"] = "urn:oid:1.3.6.1.4.1.19376.1.2.6.1"
report_class_code["code"] = "REPORT"
report_class_code["display"] = "Report"

images_class_code = {}
images_class_code["system"] = "urn:oid:1.3.6.1.4.1.19376.1.2.6.1"
images_class_code["code"] = "IMAGES"
images_class_code["display"] = "Images"

fhir = {}

Dir["#{ARGV[0]}/**/*.json"].each do |data|
	# Iterates over a directory, and loads each JSON object into a hash with
	# with the key being the resourceType of the object

	log.info("Loading: #{data}\n")
    json = JSON.parse(data_string = File.read(data))

    if fhir[json["resourceType"].to_s].nil?
    	fhir[json["resourceType"].to_s] = []
    end

    fhir[json["resourceType"].to_s] << json

end

if fhir["Patient"].nil?
	raise "Please give a patient-level directory"
end

if fhir["Patient"].length > 1
	raise "Multiple patients not currently supported"
end

# Create directories to hold our objects
patient_root_directory = File.join(Dir.pwd, ARGV[0])

FileUtils.mkpath (File.join(patient_root_directory, "DocumentReference"))
FileUtils.mkpath (File.join(patient_root_directory, "DocumentManifest"))

# Will use ERB templates to generate DocumentReference resources
# ERB template requires the following instance variables:
# @id - going to be used to uniquely identify this resource
# @div - human readable (html) rendering of the resource
# @patient_id - json
# @diagnostic_report_code

@patient_id = fhir["Patient"][0]["id"]
@patient_identifier = fhir["Patient"][0]["identifier"].to_json

reference_resources = fhir["DiagnosticReport"] + fhir["ImagingStudy"]

reference_resources.each do |r|

	@parent_resource_type = r["resourceType"]

	log.info "Processing Resource Type: #{@parent_resource_type}"

	@parent_resource_code = case @parent_resource_type
		when "DiagnosticReport"
			r["code"].to_json
		when "ImagingStudy"
			r["description"].to_json
	end

	@id = generate_id

	@parent_id = r["id"]

	@document_class_code = case @parent_resource_type
		when "DiagnosticReport"
			report_class_code.to_json
		when "ImagingStudy"
			images_class_code.to_json
	end

	@created = case @parent_resource_type
		when "DiagnosticReport"
			r["issued"]
		when "ImagingStudy"
			r["started"]
	end

	b = binding
	document_reference_template = ERB.new(File.read("document_reference.json.erb"))

	log.debug document_reference_template.result(b)

	#TODO - Create @div from the object itself

	mhd_hash = JSON.parse(document_reference_template.result(b))

	File.write(File.join(patient_root_directory,  "DocumentReference/document_reference_" + @parent_resource_type + "." + @parent_id + ".json"), JSON.pretty_generate(mhd_hash))

end