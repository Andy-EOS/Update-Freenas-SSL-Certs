import os
import requests 
import json

with open ("/path/to/certificate.pem", "r") as myfile:
    fullchain=myfile.read()

with open ("/path/to/privkey.pem", "r") as myfile:
    privkey=myfile.read()

r = requests.post(
    'https://freenashost.domain/api/v1.0/system/certificate/import/',
    auth=('root', 'FreenasPassword.'),
    headers={'Content-Type': 'application/json'},
    verify=False,
    data=json.dumps( {
        "cert_name": "Certificate Name",
        "cert_certificate": fullchain,
        "cert_privatekey": privkey,
        "cert_serial": "",
        })
    )
print r.text