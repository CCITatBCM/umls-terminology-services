import this

import requests, json
import itertools
from python_http_client import Client
from uts.settings import UMLS_SETTINGS, AVAILABLE_QUERY_PARAMS
from uts.authentication import Authenticator


authenticator = Authenticator()

base_url = 'https://uts-ws.nlm.nih.gov/rest/'
service = 'umls'

client = Client(host=base_url)


class Concept(object):
    def __init__(self, cui=None, version=None):
        self.cui = cui
        self.version = version if version else UMLS_SETTINGS['VERSION']
        self.base_resource_url = base_url + 'content/' + self.version + '/CUI/' + cui
        self.resource_url = self.base_resource_url
        self.atoms = self.Atoms()

    @staticmethod
    def build_query_params(**kwargs):
        query_params = {
            'ticket': authenticator.get_service_ticket(service),
            'language': UMLS_SETTINGS['language'],
        }

        for param in AVAILABLE_QUERY_PARAMS:
            if param in kwargs:
                query_params[param] = kwargs[param]

        return query_params

    def get(self):
        query_params = self.build_query_params()

        return handle_request(self.resource_url, params=query_params)

    def atoms(self, sabs=None, language=None, pageNumber=None, pageSize=None, ttys=None, includeObsolete=None, includeSuppressible=None):
        resource_url = self.base_resource_url + '/atoms'
        query_params = self.build_query_params(sabs=sabs, language=language, pageNumber=pageNumber, pageSize=pageSize, ttys=ttys,
                                               includeObsolete=includeObsolete, includeSuppressible=includeSuppressible)

        return handle_request(resource_url, params=query_params)

    def preferred(self, sabs=None, language=None, pageNumber=None, pageSize=None, ttys=None,
                        includeObsolete=None, includeSuppressible=None):
        resource_url = self.base_resource_url + '/atoms/preferred'
        query_params = self.build_query_params(sabs=sabs, language=language, pageNumber=pageNumber, pageSize=pageSize,
                                               ttys=ttys,
                                               includeObsolete=includeObsolete, includeSuppressible=includeSuppressible)

        return handle_request(resource_url, params=query_params)

    def definitions(self, sabs=None, pageNumber=None, pageSize=None):
        resource_url = self.base_resource_url + '/definitions'
        query_params = self.build_query_params(sabs=sabs, pageNumber=pageNumber, pageSize=pageSize)

        return handle_request(resource_url, params=query_params)

    def relations(self, sabs=None, pageNumber=None, pageSize=None):
        resource_url = self.base_resource_url + '/relations'
        query_params = self.build_query_params(sabs=sabs, pageNumber=pageNumber, pageSize=pageSize)

        return handle_request(resource_url, params=query_params)


def handle_request(url, params):
    response = requests.get(url, params=params)
    print(response.text)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return False


# def retrieve_concept(cui):
#     response = client.content.current.CUI._(cui).get(query_params=get_ticket_params())
#
#     return json.loads(response.body.decode('utf8'))['result']
#
#
# def retrieve_concept_atoms(cui, sources=''):
#     query_params = {
#         'ticket': authenticator.get_service_ticket(service),
#         'language': 'ENG'
#     }
#     if sources:
#         query_params.sabs = sources
#
#     response = requests.get(base_url + 'content/current/CUI/' + cui + '/atoms', params=query_params)
#
#     if response.status_code == 200:
#         return json.loads(response.text)
#     else:
#         return False

#     GET / content / {version} / CUI / {CUI} / atoms
#     Retrieves
#     atoms and information
#     about
#     atoms
#     for a known CUI
#
#
# GET / content / {version} / CUI / {CUI} / definitions
# Retrieves
# definitions
# for a known CUI
# GET / content / {version} / CUI / {CUI} / relations


def search():
    service_ticket = authenticator.get_service_ticket(service)
    params = {
        'ticket': service_ticket,
        'string': 'cancer',
        'sabs': 'MEDLINEPLUS',
    }
    request = requests.get(base_url + '/search/current', params=params)

    request.encoding = 'utf-8'
    items = json.loads(request.text)
    json_data = items["result"]

    print(request.text)

    page_number = 0

    while page_number < 10:
        page_number += 1
        print("Results for page " + str(page_number) + "\n")

        for result in json_data["results"]:

            try:
                print("ui: " + result["ui"])
            except NameError:
                raise NameError
            try:
                print("uri: " + result["uri"])
            except NameError:
                raise NameError
            except KeyError:
                raise KeyError
            try:
                print("name: " + result["name"])
            except NameError:
                raise NameError
            try:
                print("Source Vocabulary: " + result["rootSource"])
            except NameError:
                raise NameError

            print("\n")

            # Either our search returned nothing, or we're at the end
            if json_data["results"][0]["ui"] == "NONE":
                break
            print("*********")
