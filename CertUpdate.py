import os
import requests 
import json
from datetime import datetime

def send_new_certificate(credentials, certificate, private_key, name):
    """
    Sends a new certificate to the freenas.
    """
    r = requests.post(
        'https://freenas.theedgeofsanity.org.uk/api/v1.0/system/certificate/import/',
        auth=(credentials['user'], credentials['password']),
        headers={'Content-Type': 'application/json'},
        verify=False,
        data=json.dumps({
            "cert_name": name,
            "cert_certificate": certificate,
            "cert_privatekey": private_key,
            "cert_serial": "",
        })
    )
    print(r.text)

def list_certificates(credentials):
    """
    Requsts a list of currently installed certificates and returns the serial numbers.
    """
    r = requests.get(
        'https://freenas.theedgeofsanity.org.uk/api/v1.0/system/certificate/',
        auth=(credentials['user'], credentials['password']),
    )
    
    response_text = json.loads(r.text)
    cert_serial_numbers = []

    for x in response_text:
        cert_serial_numbers.append(x['cert_serial'])
    
    return cert_serial_numbers



with open ("/home/sysadmin/projects/Update-Freenas-SSL-Certs/.freenas_credentials", "r") as credentials_file:
    credentials = json.loads(credentials_file.read())

with open ("/home/sysadmin/projects/Update-Freenas-SSL-Certs/cert.pem", "r") as cert_file:
    fullchain=cert_file.read()

with open ("/home/sysadmin/projects/Update-Freenas-SSL-Certs/key.pem", "r") as key_file:
    privkey=key_file.read()

now = datetime.now()
cert_name = 'theedgeofsanity_' + str(now.year) + '_' + str(now.month) + '_' + str(now.day)
print(cert_name)

send_new_certificate(credentials, fullchain, privkey, cert_name)
#existing_certificate_List = list_certificates(credentials)
#print(existing_certificate_List)

