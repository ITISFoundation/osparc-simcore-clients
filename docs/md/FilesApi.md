# osparc.FilesApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**download_file**](FilesApi.md#download_file) | **GET** /v0/files/{file_id}:download | Download File
[**files_upload_multiple_view**](FilesApi.md#files_upload_multiple_view) | **GET** /v0/files/upload-multiple-view | Files Upload Multiple View
[**list_files**](FilesApi.md#list_files) | **GET** /v0/files | List Files
[**upload_multiple_files**](FilesApi.md#upload_multiple_files) | **POST** /v0/files:upload-multiple | Upload Multiple Files
[**upload_single_file**](FilesApi.md#upload_single_file) | **POST** /v0/files:upload | Upload Single File


# **download_file**
> object download_file(file_id)

Download File

### Example

```python
from __future__ import print_function
import time
import osparc
from osparc.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with osparc.ApiClient() as api_client:
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

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **files_upload_multiple_view**
> object files_upload_multiple_view()

Files Upload Multiple View

Web form to upload files at http://localhost:8000/v0/files/upload-form-view  Overcomes limitation of Swagger UI view NOTE: As of 2020-10-07, Swagger UI doesn't support multiple file uploads in the same form field

### Example

```python
from __future__ import print_function
import time
import osparc
from osparc.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with osparc.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = osparc.FilesApi(api_client)
    
    try:
        # Files Upload Multiple View
        api_response = api_instance.files_upload_multiple_view()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling FilesApi->files_upload_multiple_view: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_files**
> object list_files()

List Files

Lists all user's files 

### Example

```python
from __future__ import print_function
import time
import osparc
from osparc.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with osparc.ApiClient() as api_client:
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

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **upload_multiple_files**
> list[FileUploaded] upload_multiple_files(files)

Upload Multiple Files

### Example

```python
from __future__ import print_function
import time
import osparc
from osparc.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with osparc.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = osparc.FilesApi(api_client)
    files = '/path/to/file' # list[file] | 

    try:
        # Upload Multiple Files
        api_response = api_instance.upload_multiple_files(files)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling FilesApi->upload_multiple_files: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **files** | **list[file]**|  | 

### Return type

[**list[FileUploaded]**](FileUploaded.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **upload_single_file**
> FileUploaded upload_single_file(file)

Upload Single File

### Example

```python
from __future__ import print_function
import time
import osparc
from osparc.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with osparc.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = osparc.FilesApi(api_client)
    file = '/path/to/file' # file | 

    try:
        # Upload Single File
        api_response = api_instance.upload_single_file(file)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling FilesApi->upload_single_file: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file** | **file**|  | 

### Return type

[**FileUploaded**](FileUploaded.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

