# Patient Spec

server = YAML.load_file('fhir_server.yml')

def test_patient(server, resource)

    RSpec.describe '#put' do

        begin
            result = fhir_put(server, resource)
        rescue => e
            puts e.inspect
        end

        it {expect(result.code).to eq 200}

    end

    RSpec.describe '#get' do

        result = fhir_get(server, resource)

        it {expect(result.code).to eq 200}

        # need to remove the metadata and other keys from the server version
        json = JSON.parse(result)
        json.delete('meta')
        json.delete('lastUpdated')

        resource['managingOrganization']['reference'] = server[:url] + resource['managingOrganization']['reference']

        fhir_resource_compare(server, resource, json)

    end
end

Dir.glob("**/Patient/*") do |f|
    resource = JSON.parse(File.read(f))
    puts "Testing resource: #{f}"
    test_patient(server, resource)
end
