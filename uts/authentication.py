import requests, os, time, json
from pyquery import PyQuery
from .settings import AUTH_URL, API_KEY, SERVICES

cache_file = os.path.abspath('uts/api_cache.json')


class Authentication:

    def get_ticket_granting_ticket(self, apikey):
        now = time.time()
        cached_tgt = self.get_cached_tgt(apikey)
        print(cached_tgt)
        params = {'apikey': apikey}
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain", "User-Agent": "python"}
        request = requests.post(AUTH_URL, data=params, headers=headers)
        ticket_granting_ticket = PyQuery(request.text).find('form').attr('action')

        return ticket_granting_ticket

    def get_service_ticket(self, ticket_granting_ticket, service):
        params = {'service': SERVICES[service]}
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain", "User-Agent": "python"}
        request = requests.post(ticket_granting_ticket, data=params, headers=headers)

        return request.text

    def get_cached_tgt(self, apikey):
        print(cache_file)
        try:
            file = open('/Users/aadams/Sites/umls_terminology_services/uts/api_cache.json', 'r')
            cached = json.load(file)
            file.close(self)

            return cached[apikey]
        finally:
            return 'error'
        # print(cached)
        # file.close()
        # print(int(now - previous))
        # file = open('/Users/aadams/Sites/umls_terminology_services/tgtcache.json', 'w+')
        # data = {"1aa0bcde-b02c-4e59-b7dd-178fdc2c948e": time.time()}
        # json.dump(data, file)
        # file.close()
        # print(json.dumps(data))
