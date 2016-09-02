import os

AUTH_URL = 'https://utslogin.nlm.nih.gov/cas/v1/api-key'
API_KEY = '1aa0bcde-b02c-4e59-b7dd-178fdc2c948e'

SERVICES = {
    'umls': 'http://umlsks.nlm.nih.gov',
    'mti': 'http://skr.nlm.nih.gov/cgi-bin/SKR/Restricted_CAS/API_batchValidationII.pl',
}


UMLS_SETTINGS = {
    'AUTH_URL': 'https://utslogin.nlm.nih.gov/cas/v1/api-key',
    'SERVICES': {
        'umls': 'http://umlsks.nlm.nih.gov',
        'mti': 'http://skr.nlm.nih.gov/cgi-bin/SKR/Restricted_CAS/API_batchValidationII.pl',
    },
    'API_KEY ': os.environ.get('UMLS_API_KEY', ''),
    'LANGUAGE ': os.environ.get('UMLS_LANGUAGE', 'ENG'),
    'DEFAULT_SOURCES': os.environ.get('UMLS_DEFAULT_SOURCES', ''),
}
