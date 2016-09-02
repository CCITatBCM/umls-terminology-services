import requests, os, time, json
from pyquery import PyQuery
from uts.settings import AUTH_URL, UMLS_SETTINGS

CACHE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'api_cache.json')


class Authenticator:

    def __init__(self):
        cached_tgt = self.get_cached_tgt()

        if cached_tgt:
            self.ticket_granting_ticket = cached_tgt
        else:
            new_tgt = self.request_ticket_granting_ticket()
            cache_data = {
                'ticket_granting_ticket': new_tgt,
                'time': time.time(),
            }
            file = open(CACHE_FILE, 'w+')
            json.dump(cache_data, file)

            self.ticket_granting_ticket = new_tgt

    @staticmethod
    def request_ticket_granting_ticket():
        params = {'apikey': UMLS_SETTINGS['API_KEY']}
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain", "User-Agent": "python"}
        request = requests.post(AUTH_URL, data=params, headers=headers)
        ticket_granting_ticket = PyQuery(request.text).find('form').attr('action')

        return ticket_granting_ticket

    def get_service_ticket(self, service):
        params = {'service': UMLS_SETTINGS['SERVICES'][service]}
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain", "User-Agent": "python"}
        request = requests.post(self.ticket_granting_ticket, data=params, headers=headers)

        return request.text

    @staticmethod
    def get_cached_tgt():
        try:
            file = open(CACHE_FILE, 'r')
            cached_tgt = json.load(file)
            file.close()

            if 'time' in cached_tgt:
                # if cached ticket granting ticket is < 6 hours old
                if time.time() - cached_tgt.get('time') < 21600:
                    if cached_tgt.get('ticket_granting_ticket'):
                        return cached_tgt.get('ticket_granting_ticket')

            return False
        except:
            return False
