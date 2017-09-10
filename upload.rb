# A quick script to iterate over all of the json objects in our directory tree and post them up
# to a FHIR server

require 'bundler'
require 'yaml'
require 'logger'

log = Logger.new(STDOUT)

Bundler::require

######
#  The HAPI FHIR server requires dependent objects to be loaded first
#
######
load_order = ["Organization",
              "Medication",
              "Practitioner",
              "Patient",
              "AllergyIntolerance",
              "AdverseReaction",
              "Alert",
              "MedicationRequest",
              "MedicationDispense",
              "MedicationAdministration",
              "Observation",
              "Order",
              "OrderResponse",
              "Procedure",
              "ImagingStudy",
              "DiagnosticReport",
              "Specimen"]


if ARGV.length < 2
    raise "usage:\n\nruby upload.rb server_config.yml path_for_recursion"
end

if !File.exists?(ARGV[0])
    raise "Please specify valid yml config file"
else
    server = YAML.load_file(ARGV[0])
end

# Test a basic Get against the FHIR server
# if this fails, it throws an error and the script doesn't proceed

begin
    result = RestClient.get server[:url] + "Patient", apikey: server[:apikey], :params => {:_format => server[:format]}
rescue RestClient::ExceptionWithResponse => err
    log.error err
end

fhir = {}

Dir["#{ARGV[1]}/**/*.json"].each do |data|

    # Iterates over a directory, and loads each JSON object into a hash with
    # with the key being the resourceType of the object

    log.info("Loading: #{data}\n")

    data_string = File.read(data)

    resource = JSON.parse(File.read(data))

    id = resource["id"]

    if id.nil?
        log.error("Error reading #{data}, make sure an ID is specified in the header comment")
        raise
    end

    if fhir[resource["resourceType"].to_s].nil?
        fhir[resource["resourceType"].to_s] = []
    end

    fhir[resource["resourceType"].to_s] << resource

end

# Make sure we have load_order for all of our resource types
missing_keys = fhir.keys - load_order

if missing_keys.length > 0
  log.error("Resource Types missing from load order: #{missing_keys.inspect}")
  raise
end


load_order.each do |resource_type|

    unless fhir[resource_type].nil?
        fhir[resource_type].each do |resource|

            resource_type = resource["resourceType"]

            id = resource["id"]

            if id.nil?
                log.error("Error reading #{resource}, make sure an ID is specified in the header comment")
                raise
            end

            if id == "random"
                begin
                    url = server[:url] + resource_type
                    log.info("POST - #{url}")
                    result = RestClient.post url, resource.to_json, :content_type => server[:format] + '+fhir', :params => {:_format => server[:format]}, apikey: server[:apikey]
                rescue => e
                    raise e.response
                end
            else
                begin
                    url = server[:url] + resource_type + "/" + id
                    log.info("PUT - #{url}")
                    result = RestClient.put url, resource.to_json, :content_type => server[:format] + '+fhir', :params => {:_format => server[:format]}, apikey: server[:apikey]
                rescue => e
                    raise e.response
                end
            end
            result = JSON.parse(result)

            log.info("Submission Status: #{result["issue"][0]["diagnostics"]}")
        end
    end
end
