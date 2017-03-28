# ImagingStudy Spec

require 'rest-client'
server = YAML.load_file('fhir_server.yml')


resource = JSON.parse(File.read("siim_andy_tcga-50-5072/ImagingStudy/imaging_study.1.3.6.1.4.1.14519.5.2.1.6450.9002.159774597133442057476528099963.json"))

describe '#delete' do
	result = RestClient.delete server[:url] + resource['resourceType'] + "/" + resource['id'],
						    :params => {:_format => server[:format]}

    it {expect(result.code).to be >= 200}
    it {expect(result.code).to be <= 204}

end

describe '#put' do

    begin
        result = RestClient.put server[:url] + resource['resourceType'] + "/" + resource['id'],
                                resource.to_json,
                                :content_type => server[:format] + '+fhir',
                                :params => {:_format => server[:format]}
    rescue => e
        puts e.inspect
    end

    it {expect(result.code).to eq 200}

end

describe '#get' do

	result = RestClient.get server[:url] + resource['resourceType'] + "/" + resource['id'],
						    :params => {:_format => server[:format]}

	it {expect(result.code).to eq 200}

	# need to remove the metadata and other keys from the server version
	json = JSON.parse(result)
	json.delete('meta')
	json.delete('lastUpdated')

	resource['patient']['reference'] = server[:url] + resource['patient']['reference']

	it {expect(json).to eq resource}

end
