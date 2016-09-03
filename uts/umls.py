import requests, json
from python_http_client import Client
from uts.settings import UMLS_SETTINGS, AVAILABLE_QUERY_PARAMS
from uts.authentication import Authenticator
from collections import abc

BASE_URL = 'https://uts-ws.nlm.nih.gov/rest/'
SERVICE = 'umls'

authenticator = Authenticator()
client = Client(host=BASE_URL)


class Content:
    def __init__(self, resource_url, sabs=None, language=None,
                 page_number=None, page_size=None, ttys=None,
                 include_obsolete=None, include_suppressible=None):
        self.resource_url = resource_url
        self.response = handle_request(
            self.resource_url,
            params=build_query_params(
                sabs=sabs,
                language=language,
                pageNumber=page_number,
                pageSize=page_size,
                ttys=ttys,
                includeObsolete=include_obsolete,
                includeSuppressible=include_suppressible
            )
        )
        if self.response is not False:
            self.__data = self.response
        else:
            self.__data = {}

    def __getattr__(self, name):
        if hasattr(self.__data, name):
            return getattr(self.__data, name)
        elif name in self.__data:
            return self.__data[name]
        else:
            return Content.build(self.__data[name])

    @classmethod
    def build(cls, obj):
        print(obj)
        if isinstance(obj, abc.Mapping):
            return cls(obj)
        elif isinstance(obj, abc.MutableSequence):
            return [cls.build(item) for item in obj]
        else:
            return obj


class Concept(Content):
    def __init__(self, cui=None, version=None):
        self.cui = cui
        self.version = version if version else UMLS_SETTINGS['VERSION']
        self.resource_url = BASE_URL + 'content/' + self.version + '/CUI/' + cui
        Content.__init__(self, self.resource_url)

    def atoms(self, **kwargs):
        return Content(self.resource_url + '/atoms', kwargs)

    def atoms_preferred(self, **kwargs):
        return Content(self.resource_url + '/atoms/preferred', kwargs)

    def definitions(self, **kwargs):
        return Content(self.resource_url + '/definitions', kwargs)

    def relations(self, **kwargs):
        return Content(self.resource_url + '/relations', kwargs)


def build_query_params(**kwargs):
    query_params = {
        'ticket': authenticator.get_service_ticket(SERVICE),
        'language': UMLS_SETTINGS['language'],
    }

    for param in AVAILABLE_QUERY_PARAMS:
        if param in kwargs:
            query_params[param] = kwargs[param]

    return query_params


def handle_request(url, params):
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return False


def search():
    service_ticket = authenticator.get_service_ticket(SERVICE)
    params = {
        'ticket': service_ticket,
        'string': 'cancer',
        'sabs': 'MEDLINEPLUS',
    }
    request = requests.get(BASE_URL + '/search/current', params=params)

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
