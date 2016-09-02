import requests, json
from python_http_client import Client
from uts.authentication import Authenticator


authenticator = Authenticator()

base_url = 'https://uts-ws.nlm.nih.gov/rest/'
service = 'umls'

client = Client(host=base_url)


def get_ticket_params():
    return {
        'ticket': authenticator.get_service_ticket(service),
    }


def retrieve_concept(cui):
    response = client.content.current.CUI._(cui).get(query_params=get_ticket_params())

    return json.loads(response.body.decode('utf8'))['result']


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

    pagenumber = 0

    while pagenumber < 10:
        pagenumber += 1
        print("Results for page " + str(pagenumber) + "\n")

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

print(retrieve_concept('C0009044'))
