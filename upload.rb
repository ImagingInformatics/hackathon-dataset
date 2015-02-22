# A quick script to iterate over all of the json objects in our directory tree and post them up
# to a FHIR server

require 'bundler'
require 'yaml'
require 'logger'

log = Logger.new(STDOUT)

Bundler::require

if !File.exists?("fhir_server.yml")
	raise "Please edit fhir_server.yml"
else
	s = YAML.load_file("fhir_server.yml")
end

# Test a basic Get against the FHIR server
# if this fails, it throws an error and the script doesn't proceed

begin
	result = RestClient.get s[:url] + "Patient", :params => {:_format => s[:format]}
rescue
	log.error(result)
	raise
end

Dir["./**/*.json"].each do |data|

	log.info("Processing: #{data}\n")

	data_string = File.read(data)

	begin
		# find the ID from the comment at the top of the JSON file
		id = data_string.scan(/id:(.*?)$/).first.first.strip!
	rescue
		log.error("Error reading #{data}, make sure an ID is specified in the header comment")
		raise 
	end

	resource_type = JSON.parse(data_string)["resourceType"]

	if id == "random"
		begin
			result = RestClient.post s[:url] + resource_type, data_string, :content_type => s[:format] + '+fhir', :params => {:_format => s[:format]}
		rescue => e
			e.response
		end
	else
		begin
			result = RestClient.put s[:url] + resource_type + "/" + id, data_string, :content_type => s[:format] + '+fhir', :params => {:_format => s[:format]}
		rescue => e
			e.response
		end
	end
end
