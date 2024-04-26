import requests
import xml.etree.ElementTree as ET

def get_data(api, domain_list):
    response = requests.get(api)
    
    if response.status_code == 200:
        return process_response(response.text, domain_list)
    else:
        print(f"Error: {response.status_code}. Failed to fetch data.")
        print("Response content:", response.content)
        return []

def process_response(xml_text, domain_list):
    root = ET.fromstring(xml_text)

    available_domains = []

    for domain_result in root.findall('.//{http://api.namecheap.com/xml.response}DomainCheckResult'):
        domain_name = domain_result.attrib.get('Domain')
        available = domain_result.attrib.get('Available') == 'true'

        if available:
            available_domains.append(domain_name)

    return available_domains

def make_api_call(domain, domain_extension):
    api = f"https://api.namecheap.com/xml.response?ApiUser=swipeconnect&ApiKey=00a7b6e8e31c42a785fe56959c7103ef&UserName=swipeconnect&Command=namecheap.domains.check&ClientIp=27.58.176.15&DomainList={domain+domain_extension}"
    return api

if __name__ == "__main__":
    domain = "facebook12345"
    domain_extensions = [".com",".in",".org",".net",".us",".xyz",".online",".info"]
    available_domains = []
    
    print("Loading...")
    
    for extension in domain_extensions:
        api_url = make_api_call(domain, extension)
        available_domains.extend(get_data(api_url, available_domains))
    
    print("Available domains:", available_domains)
