# A quick script to iterate over all of the json objects in our directory tree and post them up
# to a FHIR server

require 'bundler'
require 'yaml'
require 'logger'

log = Logger.new(STDOUT)

Bundler::require

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
rescue
	log.error(result)
	raise
end

Dir["#{ARGV[1]}/**/*.json"].each do |data|

	log.info("Processing: #{data}\n")

	data_string = File.read(data)

	resource = JSON.parse(File.read(data))

	id = resource["id"]

	if id.nil?
		log.error("Error reading #{data}, make sure an ID is specified in the header comment")
		raise 
	end

	resource_type = resource["resourceType"]

	log.debug("Resource: #{resource.to_json}\n\nResource Type: #{resource_type}")

	if id == "random"
		begin
			result = RestClient.post server[:url] + resource_type, resource.to_json, :content_type => server[:format] + '+fhir', :params => {:_format => server[:format]}, apikey: server[:apikey]
		rescue => e
			e.response
		end
	else
		begin
			result = RestClient.put server[:url] + resource_type + "/" + id, resource.to_json, :content_type => server[:format] + '+fhir', :params => {:_format => server[:format]}, apikey: server[:apikey]
		rescue => e
			e.response
		end
	end
end
