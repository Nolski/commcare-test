import os
import requests
import json

from requests.auth import HTTPBasicAuth, HTTPDigestAuth


class CommCareApi():
    def __init__(self):
        self._username = os.environ.get('COMMCARE_USERNAME')
        self._password = os.environ.get('COMMCARE_PASSWORD')
        self._api_version = 'v0.4'
        self._domain = os.environ.get('COMMCARE_DOMAIN')
        self._domain_url = f"https://www.commcarehq.org/a/{self._domain}/api"

    def list_forms(self):
        forms = self.get_request(self._domain_url, "form")
        print(json.dumps(forms, sort_keys=True))

    def get_request(self, domain, action,
                    query_params={},
                    include_version=True,
                    unpack=lambda r: r.json()):
        if include_version:
            url = f"{domain}/{self._api_version}/{action}/"
        else:
            url = f"{domain}/{action}/"

        query = "&".join([k + "=" + v for k, v in query_params.items()])
        if query is not "":
            url += "?" + query

        r = requests.get(
            url=url,
            auth=HTTPBasicAuth(self._username, self._password)
        )

        if r.status_code == 200:
            return unpack(r)
        else:
            error_msg = f"Request {url} failed (code {r.status_code})"
            raise Exception(error_msg)


def main():
    api = CommCareApi()
    api.list_forms()

if __name__ == '__main__':
    main()
