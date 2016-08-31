import requests, json, time, os
from pyquery import PyQuery


class Authentication:
    def __init__(self):
        now = time.time()
        file = open('/Users/aadams/Sites/umls_terminology_services/tgtcache.json', 'r')
        cached = json.load((file))

        previous = cached['1aa0bcde-b02c-4e59-b7dd-178fdc2c948e']
        print(cached)
        file.close()
        print(int(now - previous))
        file = open('/Users/aadams/Sites/umls_terminology_services/tgtcache.json', 'w+')
        data = {"1aa0bcde-b02c-4e59-b7dd-178fdc2c948e": time.time()}
        json.dump(data, file)
        file.close()
        print(json.dumps(data))



def get_ticket_granting_ticket(apikey):
    params = {'apikey': apikey}
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain", "User-Agent": "python"}
    request = requests.post('https://utslogin.nlm.nih.gov/cas/v1/api-key', data=params, headers=headers)
    ticket_granting_ticket = PyQuery(request.text).find('form').attr('action')

    return ticket_granting_ticket


temp = Authentication()


