import os

from json import dumps, loads
from re import search
from typing import List

from requests import get, post, put, delete

SAUCE_API_ENDPOINT = 'https://api.us-west-1.saucelabs.com/v1'

REQUESTS = {
    'GET': get,
    'POST': post,
    'PUT': put,
    'DELETE': delete
}


class SauceException(Exception):
    pass


class SauceStorageApi:
    """
    Args:
        - username: str - username from saucelabs
        - access_key: str - access_key from saucelabs
        - sauce_api_endpoint: str - api endpoint you want to use if default
          https://api.us-west-1.saucelabs.com/v1 not serve your propose
    """
    username: str
    access_key: str
    sauce_api_endpoint: str
    remote_app: dict

    def __init__(
        self, username: str, access_key: str,
        sauce_api_endpoint: str = SAUCE_API_ENDPOINT
    ):
        self.username = username
        self.access_key = access_key
        self.sauce_api_endpoint = sauce_api_endpoint

    def get_method_url(self, group: str, path: str = None, query: str = None):
        """
        Genarate url by method called

        Args:
            - group: str
            - path: str = None
            - query: str = None
        Return str
        """
        url = f'{self.sauce_api_endpoint}/{group}'
        if path:
            url += f'/{path}'
        if query:
            url += f'/{query}'
        return url

    def get_remote_name(self, file_path: str, remote_name: str):
        """
        Check if remote_name is been pass if not return base_name of apk as
        remote_name

        Args:
            - file_path : str
            - remote_name: str
        Return str
        """
        if remote_name is None:
            remote_name = os.path.basename(file_path)
        return remote_name

    def request(self, url, body=None, files=None, params=None,
                method: str = 'GET'):
        if method == 'GET':
            response = REQUESTS[method](
                url,
                params=params,
                auth=(self.username, self.access_key)
            )
        else:
            response = REQUESTS[method](
                url,
                data=body,
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

    def upload(self, file_path: str, remote_name: str = None) -> dict:
        """
        Upload your app to Saucelabs.

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
            self.remote_app = json_data
            return self.remote_app

    def download(self, file_id: str, output_path: str) -> str:
        """
        Download specific app by file_id.

        Args:
            - file_id: str - File identifier supplied by Sauce Labs.
            - output_path: str - Folder where downloaded file will be save.
        """
        url = self.get_method_url('storage', 'download', file_id)
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

    def edit(self, file_id: str, body: List) -> list:
        """
        Edit information in specific app by file_id

        Args:
            - file_id: str - File identifier supplied by Sauce Labs.
            - body: List - Itens you want to change in app
        Return: List
        """
        url = self.get_method_url('storage', 'files', file_id)
        json_data = self.request(url, body=dumps(body), method='PUT')
        return json_data

    def delete_app(self, file_id: str = None, group_id: str = None) -> list:
        """
        Delete specific app by file_id or delete group of apps by group_id

        Args:
            - file_id: str - File identifier supplied by Sauce Labs.
            - group_id: str - Group identifier supplied by Sauce Labs.
        Return: list
        """
        if file_id:
            url = self.get_method_url('storage', 'files', file_id)
        if group_id:
            url = self.get_method_url('storage', 'groups', group_id)
        json_data = self.request(url, method='DELETE')
        return json_data

    def files(self, q: str = None, kind: str = None, file_id: str = None,
              team_id: str = None, page: int = 1, per_page: int = 25):
        """
        List uploaded files by follow parameters

        Args:
            - q: str = None - Search term (semantic version, build number,
            file name, app name, app identifier, etc.)
            - kind: str = None - ios, android, other
            - file_id: str = None - One or more group ids to be listed
            - team_id: str = None - One or more team ids the listed file(s)
            should be shared with
            - page: int = 1 - The number of the current page to show, by
            default it starts from one
            - per_page: int = 25 - The count of items per listed page. By
            default it is 25, and the acceptable range is 1-100
        """
        default_params = {
            'q': q, 'kind': kind, 'file_id': file_id,
            'team_id': team_id, 'page': page, 'per_page': per_page
        }
        params = {
            key: value for key, value in default_params.items()
            if value is not None
        }
        url = self.get_method_url('storage', 'files')

        return self.request(url, params=params)

    def groups(self, q: str = None, kind: str = None, file_id: str = None,
               page: int = 1, per_page: int = 25):
        """
        List group of app by follow parameters
        Args:
            - q: str = None - Search term (semantic version, build number,
            file name, app name, app identifier, etc.)
            - kind: str = None - ios, android, other
            - file_id: str = None - One or more group ids to be listed
            - page: int = 1 - The number of the current page to show, by
            default it starts from one
            - per_page: int = 25 - The count of items per listed page. By
            default it is 25, and the acceptable range is 1-100
        """
        default_params = {
            'q': q, 'kind': kind, 'file_id': file_id, 'page': page,
            'per_page': per_page
        }
        params = {
            key: value for key, value in default_params.items()
            if value is not None
        }
        url = self.get_method_url('storage', 'groups')

        return self.request(url, params=params)
    
    def get_file_id():
        return self.remote_app['item']['id']
