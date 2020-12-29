from base64 import b64encode
from json import loads
from requests import post

SAUCE_API_ENDPOINT = 'https://api.us-west-1.saucelabs.com/v1'

REQUESTS = {
    'POST': post
}


class SauceException(Exception):
    pass


class SauceStorageApi(object):
    """
    Args:
        - username: str - username from saucelabs
        - access_key: str - access_key from saucelabs
        - sauce_api_endpoint: str - api endpoint you want to use if default
          https://api.us-west-1.saucelabs.com/v1 not serve your propose
    """

    def __init__(
        self, username: str, access_key: str,
        sauce_api_endpoint: str = SAUCE_API_ENDPOINT
    ):
        self.username = username
        self.access_key = access_key
        self.sauce_api_endpoint = sauce_api_endpoint

    def get_method_url(self, group, path=None, query=None):
        url = f'{self.sauce_api_endpoint}/storage/{group}'
        # if path is not None:
        #    url = url + '/' + path
        # if query is not None:
        #    url = url + '?' + urlencode(query)
        return url

    def request(self, url, body=None, files=None, method: str = 'GET'):
        response = REQUESTS[method](
            url,
            data=body,
            files=files,
            auth=(self.username, self.access_key)
        )
        if response.status_code >= 200 and response.status_code < 300:
            return loads(response.text)
        else:
            raise SauceException(
                'Sauce Status NOT OK'
                f'{response.status_code}: {response.text}'
            )

    def post(self, file_path, remote_name=None):
        url = self.get_method_url('upload')
        with open(file_path, 'rb') as file:
            files = {
                'payload': file,
                'file_name': remote_name
            }
            json_data = self.request(
                url=url,
                files=files,
                method='POST'
            )
            return json_data
