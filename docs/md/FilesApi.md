# osparc.FilesApi

All URIs are relative to *https://api.osparc.io*

Method | HTTP request | Description
------------- | ------------- | -------------
[**download_file**](FilesApi.md#download_file) | **GET** /v0/files/{file_id}/content | Download File
[**get_file**](FilesApi.md#get_file) | **GET** /v0/files/{file_id} | Get File
[**list_files**](FilesApi.md#list_files) | **GET** /v0/files | List Files
[**upload_file**](FilesApi.md#upload_file) | **PUT** /v0/files/content | Upload File


# **download_file**

> file download_file(file_id)

Download File

### Example

* Basic Authentication (HTTPBasic):

```python
from __future__ import print_function
import time
import osparc
from osparc.rest import ApiException
from pprint import pprint
configuration = osparc.Configuration()
# Configure HTTP basic authorization: HTTPBasic
configuration.username = 'YOUR_API_KEY_HERE'
configuration.password = 'YOUR_API_SECRET_HERE'

# Defining host is optional and default to https://api.osparc.io
configuration.host = "https://api.osparc.io"
# Enter a context with an instance of the API client
with osparc.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = osparc.FilesApi(api_client)
    file_id = 'file_id_example' # str | 

    try:
        # Download File
        api_response = api_instance.download_file(file_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling FilesApi->download_file: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file_id** | [**str**](.md)|  | 

### Return type

**file**

### Authorization

[HTTPBasic](../README.md#HTTPBasic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/octet-stream, text/plain, application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Returns a arbitrary binary data |  -  |
**404** | File not found |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_file**

> File get_file(file_id)

Get File

Gets metadata for a given file resource 

### Example

* Basic Authentication (HTTPBasic):

```python
from __future__ import print_function
import time
import osparc
from osparc.rest import ApiException
from pprint import pprint
configuration = osparc.Configuration()
# Configure HTTP basic authorization: HTTPBasic
configuration.username = 'YOUR_API_KEY_HERE'
configuration.password = 'YOUR_API_SECRET_HERE'

# Defining host is optional and default to https://api.osparc.io
configuration.host = "https://api.osparc.io"
# Enter a context with an instance of the API client
with osparc.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = osparc.FilesApi(api_client)
    file_id = 'file_id_example' # str | 

    try:
        # Get File
        api_response = api_instance.get_file(file_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling FilesApi->get_file: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file_id** | [**str**](.md)|  | 

### Return type

[**File**](File.md)

### Authorization

[HTTPBasic](../README.md#HTTPBasic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**404** | File not found |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_files**

> list[File] list_files()

List Files

Lists all files stored in the system  

### Example

* Basic Authentication (HTTPBasic):

```python
from __future__ import print_function
import time
import osparc
from osparc.rest import ApiException
from pprint import pprint
configuration = osparc.Configuration()
# Configure HTTP basic authorization: HTTPBasic
configuration.username = 'YOUR_API_KEY_HERE'
configuration.password = 'YOUR_API_SECRET_HERE'

# Defining host is optional and default to https://api.osparc.io
configuration.host = "https://api.osparc.io"
# Enter a context with an instance of the API client
with osparc.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = osparc.FilesApi(api_client)
    
    try:
        # List Files
        api_response = api_instance.list_files()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling FilesApi->list_files: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[File]**](File.md)

### Authorization

[HTTPBasic](../README.md#HTTPBasic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **upload_file**

> File upload_file(file, content_length=content_length)

Upload File

Uploads a single file to the system

### Example

* Basic Authentication (HTTPBasic):

```python
from __future__ import print_function
import time
import osparc
from osparc.rest import ApiException
from pprint import pprint
configuration = osparc.Configuration()
# Configure HTTP basic authorization: HTTPBasic
configuration.username = 'YOUR_API_KEY_HERE'
configuration.password = 'YOUR_API_SECRET_HERE'

# Defining host is optional and default to https://api.osparc.io
configuration.host = "https://api.osparc.io"
# Enter a context with an instance of the API client
with osparc.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = osparc.FilesApi(api_client)
    file = '/path/to/file' # file | 
content_length = 'content_length_example' # str |  (optional)

    try:
        # Upload File
        api_response = api_instance.upload_file(file, content_length=content_length)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling FilesApi->upload_file: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file** | **file**|  | 
 **content_length** | **str**|  | [optional] 

### Return type

[**File**](File.md)

### Authorization

[HTTPBasic](../README.md#HTTPBasic)

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

