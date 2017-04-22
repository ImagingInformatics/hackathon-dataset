# MedicationOrder Spec

server = YAML.load_file('fhir_server.yml')

resource = JSON.parse(File.read("siim_sally-breastdx-01-0003/MedicationOrder/medication_order.breastdx.json"))

RSpec.describe '#delete' do
    result = fhir_delete(server, resource)
    it {expect(result.code).to be >= 200}
    it {expect(result.code).to be <= 204}

end

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

    resource['patient']['reference'] = server[:url] + resource['patient']['reference']
    resource['prescriber']['reference'] = server[:url] + resource['prescriber']['reference']
    resource['medicationReference']['reference'] = server[:url] + resource['medicationReference']['reference']

    it {expect(json).to eq resource}

end
