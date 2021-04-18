# Sauce Application Storage

This repository has the purpose of abstracting the use of the Application Store of Sauce Labs for real devices tests - https://wiki.saucelabs.com/display/DOCS/Application+Storage


## Usage

### Instantiate 
```python
from sauce_storage_api import SauceStorageApi

sauce_api = SauceStorageApi(
    username='<username>',
    access_key='<access_key>'
)
```
if you need different endpoint of  ```https://api.us-west-1.saucelabs.com/v1```
```python
from sauce_storage_api import SauceStorageApi

sauce_api = SauceStorageApi(
    username='<username>',
    access_key='<access_key>',
    sauce_api_endpoint='<your_sauceserver_endpoint>'
)
```

### Upload your app
#### For upload your app to application storage
```python
sauce_api.upload(
    '<app_path>'
)
```
#### If you want to save your app with a different name of your computer
```python
sauce_api.upload(
    '<app_path>',
    '<remote_name>'
)
```

<br />
#### Get App Id
```
sauce_api.get_file_id()
```

<br />

### Download uploaded app
#### If you need to download your app 
```python
sauce_api.download(
    '<file_id>',
)
```

<br />

### Edit uploaded app informations
#### If your need to upload some info of your app
```python
response = api.edit(
    '<file_id>',
    {'item': {'description':'string'}}
)
```

<br />
#### Response will you get will be something like this
```json
{
   "item":{
      "id": "str",
      "owner":{
         "id": "str",
         "org_id": "str"
      },
      "name": "str",
      "upload_timestamp": "timestamp",
      "etag": "str",
      "kind": "str",
      "group_id": "int",
      "description": "str",
      "metadata":{
         "identifier": "str",
         "name": "str",
         "version": "str",
         "is_test_runner": "bool",
         "icon": "str",
         "version_code": "int",
         "min_sdk": "int",
         "target_sdk": "int"
      },
      "access":{
         "team_ids":[
            "str"
         ],
         "org_ids":[
            "str"
         ]
      }
   },
   "changed": true
}
```
#### Warning !
#### The SauceLabs documentation doesn't explicit the fields you can change, so try your luck

<br />

### Delete App
#### If want delete specific file
```python
response = api.delete_app(file_id='<file_id>')
```
#### If want delete specific group of files
```python
response = api.delete_app(group_id='<group_id>')
```

<br />

### Files
#### If want to list all your files and properties
```python
api.files(
   q='<query>',
   kind='<kind>',
   file_id='<file_id>',
   team_id='<team_id>',
   page='<page>', 
   per_page='<per_page>'
)
```

<br />

### Groups (App)
#### If want to list all your app's grouped and properties
```python
api.files(
   q='<query>',
   kind='<kind>',
   file_id='<file_id>',
   team_id='<team_id>',
   page='<page>', 
   per_page='<per_page>'
)
```
