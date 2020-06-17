# osparc.UsersApi

All URIs are relative to *http://localhost*

| Method                                                 | HTTP request   | Description       |
| ------------------------------------------------------ | -------------- | ----------------- |
| [**get_my_profile**](UsersApi.md#get_my_profile)       | **GET** /v0/me | Get My Profile    |
| [**update_my_profile**](UsersApi.md#update_my_profile) | **PUT** /v0/me | Update My Profile |


# **get_my_profile**
> Profile get_my_profile()

Get My Profile

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
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# Defining host is optional and default to http://localhost
configuration.host = "http://localhost"
# Enter a context with an instance of the API client
with osparc.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = osparc.UsersApi(api_client)

    try:
        # Get My Profile
        api_response = api_instance.get_my_profile()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling UsersApi->get_my_profile: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**Profile**](Profile.md)

### Authorization

[HTTPBasic](../README.md#HTTPBasic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description         | Response headers |
| ----------- | ------------------- | ---------------- |
| **200**     | Successful Response | -                |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_my_profile**
> Profile update_my_profile(profile_update)

Update My Profile

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
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# Defining host is optional and default to http://localhost
configuration.host = "http://localhost"
# Enter a context with an instance of the API client
with osparc.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = osparc.UsersApi(api_client)
    profile_update = osparc.ProfileUpdate() # ProfileUpdate |

    try:
        # Update My Profile
        api_response = api_instance.update_my_profile(profile_update)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling UsersApi->update_my_profile: %s\n" % e)
```
[Download UsersApi.ipynb](code_samples/UsersApi.ipynb ':ignore:')


### Parameters

| Name               | Type                                  | Description | Notes |
| ------------------ | ------------------------------------- | ----------- | ----- |
| **profile_update** | [**ProfileUpdate**](ProfileUpdate.md) |             |

### Return type

[**Profile**](Profile.md)

### Authorization

[HTTPBasic](../README.md#HTTPBasic)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description         | Response headers |
| ----------- | ------------------- | ---------------- |
| **200**     | Successful Response | -                |
| **422**     | Validation Error    | -                |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


