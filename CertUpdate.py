import os
import requests 
import json
from datetime import datetime
import time

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

def list_certificates(credentials):
    """
    Requsts a list of currently installed certificates and returns the serial numbers.
    """
    r = requests.get(
        'https://freenas.theedgeofsanity.org.uk/api/v1.0/system/certificate/',
        auth=(credentials['user'], credentials['password']),
    )
    
    response = json.loads(r.text)
    cert_serial_numbers = []

    return response

def set_certificate_as_active(credentials, cert_id):
    """
    Sets a certificate as the currently active certificate.
    """
    r = requests.put(
        'https://freenas.theedgeofsanity.org.uk/api/v1.0/system/settings/',
        auth=(credentials['user'], credentials['password']),
        headers={'Content-Type': 'application/json'},
        data=json.dumps({
            "stg_guicertificate": cert_id,
        }),
    )

def delete_certificate(credentials, cert_id):
    """
    Delete a certificate
    """
    r = requests.delete(
        'https://freenas.theedgeofsanity.org.uk/api/v1.0/system/certificate/' + str(cert_id) + '/',
        auth=(credentials['user'], credentials['password']),
        headers={'Content-Type': 'application/json'}
    )

def restart_web_service(credentials):
    """
    Restart the webserver.
    """
    try:
        r = requests.post(
            'https://freenas.theedgeofsanity.org.uk/api/v1.0/system/settings/restart-httpd-all/',
            auth=(credentials['user'], credentials['password']),
        )
    except requests.exceptions.ConnectionError:
        pass #This error is expected when restarting the webserver

## Open a file containing the root login.
with open ("/path/to/credentials", "r") as credentials_file:
    credentials = json.loads(credentials_file.read())

## Get the certificate from the cert file.
with open ("/path/to/certificate", "r") as cert_file:
    fullchain=cert_file.read()

## Get the private key from the key file.
with open ("/path/to/privat key", "r") as key_file:
    privkey=key_file.read()

## Name the certificate using the current date.
now = datetime.now()
new_cert_name = 'theedgeofsanity_' + str(now.year) + '_' + str(now.month) + '_' + str(now.day)

## Send the new certificate to the freenas
send_new_certificate(credentials, fullchain, privkey, new_cert_name)

## Retreive a list of installed certificates
certificate_List = list_certificates(credentials)

## Find the certificate with the correct name & set it is the live certificate.
for cert in certificate_List:
    if(cert['cert_name'] == new_cert_name):
        set_certificate_as_active(credentials, cert['id'])

## Restart the web server (the certificate change will not take effect without this)
restart_web_service(credentials)

## Allow time for the server to restart (usually takes a few seconds. 60 is overkill.)
time.sleep(60)

## Delete all certificates except the one we have just installed.
for cert in certificate_List:
    if(cert['cert_name'] != new_cert_name):
        delete_certificate(credentials, cert['id'])