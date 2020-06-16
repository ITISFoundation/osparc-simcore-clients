# osparc.MetaApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_service_metadata**](MetaApi.md#get_service_metadata) | **GET** /v0/meta | Get Service Metadata


# **get_service_metadata**
> AnyOfMetastring get_service_metadata(extended_info=extended_info)

Get Service Metadata

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
    api_instance = osparc.MetaApi(api_client)
    extended_info = False # bool |  (optional) (default to False)

    try:
        # Get Service Metadata
        api_response = api_instance.get_service_metadata(extended_info=extended_info)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling MetaApi->get_service_metadata: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **extended_info** | **bool**|  | [optional] [default to False]

### Return type

[**AnyOfMetastring**](AnyOfMetastring.md)

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

