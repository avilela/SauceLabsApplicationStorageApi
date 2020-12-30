import os

from json import dumps, loads
from httpx import get, post, put
from re import search
from typing import List

SAUCE_API_ENDPOINT = 'https://api.us-west-1.saucelabs.com/v1'

REQUESTS = {
    'GET': get,
    'POST': post,
    'PUT': put
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
        url = f'{self.sauce_api_endpoint}/{group}'
        if path:
            url += f'/{path}'
        if query:
            url += f'/{query}'
        return url

    def get_remote_name(self, file_path, remote_name):
        """
        Check if remote_name is been pass if not return base_name of apk as
        remote_name
        Args:
            - file_path
            - remote_name
        Return str
        """
        if remote_name is None:
            remote_name = os.path.basename(file_path)
        return remote_name

    def request(self, url, body=None, files=None, method: str = 'GET'):
        if method == 'GET':
            response = REQUESTS[method](
                url,
                auth=(self.username, self.access_key)
            )
        else:
            response = REQUESTS[method](
                url,
                data=dumps(body),
                files=files,
                auth=(self.username, self.access_key)
            )
        if (response.status_code >= 200 and response.status_code < 300
                and method != 'GET'):
            return loads(response.text)
        elif method == 'GET':
            return response
        else:
            raise SauceException(
                'Sauce Status NOT OK\n'
                f'{response.status_code}: {response.text}'
            )

    def upload(self, file_path, remote_name=None) -> list:
        """
        Args:
            - file_path: str - File path in host
            - remote_name: str - App name will be in saucelabs
        Return: list
        """
        url = self.get_method_url('storage', 'upload')
        remote_name = self.get_remote_name(file_path, remote_name)
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

    def download(self, file_id: str, output_path: str) -> str:
        """
        Args:
            - file_id: str - File identifier supplied by Sauce Labs.
            - output_path: str - Folder where downloaded file will be save.
        """
        url = self.get_method_url('download', file_id)
        response = self.request(
            url=url,
            method='GET'
        )
        file_name = search(
            r'\"(.*?)\"', response.headers['content-disposition']
        ).group(1)
        with open(f'{output_path}/{file_name}', 'wb') as file:
            file.write(response.content)

        return f'{output_path}/{file_name}'

    def edit(self, file_id: str, body: List):
        """
        Args:
            - file_id: str - File identifier supplied by Sauce Labs.
            - body: List - Itens you want to change in app 
        """
        url = self.get_method_url('storage', 'files', file_id)
        json_data = self.request(url, body=body, method='PUT')
        return json_data
