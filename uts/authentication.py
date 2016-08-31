import requests
from pyquery import PyQuery
from .settings import AUTH_URL, API_KEY


class Authentication:
    def __init__(self, service):
        self.service = service

    def get_ticket_granting_ticket(self):
        params = {'apikey': API_KEY}
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain", "User-Agent": "python"}
        request = requests.post(AUTH_URL, data=params, headers=headers)

        # extract the entire URL needed from the HTML form (action attribute) returned
        # looks similar to
        # https://utslogin.nlm.nih.gov/cas/v1/tickets/TGT-36471-aYqNLN2rFIJPXKzxwdTNC5ZT7z3B3cTAKfSc5ndHQcUxeaDOLN-cas
        # we make a POST call to this URL in the getst method

        ticket_granting_ticket = PyQuery(request.text).find('form').attr('action')

        return ticket_granting_ticket
