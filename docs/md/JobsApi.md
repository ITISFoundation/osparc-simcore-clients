# osparc.JobsApi

All URIs are relative to *https://api.osparc.io*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_job**](JobsApi.md#get_job) | **GET** /v0/jobs/{job_id} | Get Job
[**get_job_output**](JobsApi.md#get_job_output) | **GET** /v0/jobs/{job_id}/outputs/{output_name} | Get Job Output
[**inspect_job**](JobsApi.md#inspect_job) | **POST** /v0/jobs/{job_id}:inspect | Inspect Job
[**list_all_jobs**](JobsApi.md#list_all_jobs) | **GET** /v0/jobs | List All Jobs
[**list_job_outputs**](JobsApi.md#list_job_outputs) | **GET** /v0/jobs/{job_id}/outputs | List Job Outputs
[**start_job**](JobsApi.md#start_job) | **POST** /v0/jobs/{job_id}:start | Start Job
[**stop_job**](JobsApi.md#stop_job) | **POST** /v0/jobs/{job_id}:stop | Stop Job


# **get_job**
> Job get_job(job_id)

Get Job

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
    api_instance = osparc.JobsApi(api_client)
    job_id = 'job_id_example' # str | 

    try:
        # Get Job
        api_response = api_instance.get_job(job_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling JobsApi->get_job: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **job_id** | [**str**](.md)|  | 

### Return type

[**Job**](Job.md)

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

# **get_job_output**
> JobOutput get_job_output(job_id, output_name)

Get Job Output

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
    api_instance = osparc.JobsApi(api_client)
    job_id = 'job_id_example' # str | 
output_name = 'output_name_example' # str | 

    try:
        # Get Job Output
        api_response = api_instance.get_job_output(job_id, output_name)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling JobsApi->get_job_output: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **job_id** | [**str**](.md)|  | 
 **output_name** | **str**|  | 

### Return type

[**JobOutput**](JobOutput.md)

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

# **inspect_job**
> JobStatus inspect_job(job_id)

Inspect Job

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
    api_instance = osparc.JobsApi(api_client)
    job_id = 'job_id_example' # str | 

    try:
        # Inspect Job
        api_response = api_instance.inspect_job(job_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling JobsApi->inspect_job: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **job_id** | [**str**](.md)|  | 

### Return type

[**JobStatus**](JobStatus.md)

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

# **list_all_jobs**
> list[Job] list_all_jobs()

List All Jobs

List of all jobs created by user 

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
    api_instance = osparc.JobsApi(api_client)
    
    try:
        # List All Jobs
        api_response = api_instance.list_all_jobs()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling JobsApi->list_all_jobs: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[Job]**](Job.md)

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

# **list_job_outputs**
> list[JobOutput] list_job_outputs(job_id)

List Job Outputs

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
    api_instance = osparc.JobsApi(api_client)
    job_id = 'job_id_example' # str | 

    try:
        # List Job Outputs
        api_response = api_instance.list_job_outputs(job_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling JobsApi->list_job_outputs: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **job_id** | [**str**](.md)|  | 

### Return type

[**list[JobOutput]**](JobOutput.md)

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

# **start_job**
> JobStatus start_job(job_id)

Start Job

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
    api_instance = osparc.JobsApi(api_client)
    job_id = 'job_id_example' # str | 

    try:
        # Start Job
        api_response = api_instance.start_job(job_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling JobsApi->start_job: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **job_id** | [**str**](.md)|  | 

### Return type

[**JobStatus**](JobStatus.md)

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

# **stop_job**
> Job stop_job(job_id)

Stop Job

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
    api_instance = osparc.JobsApi(api_client)
    job_id = 'job_id_example' # str | 

    try:
        # Stop Job
        api_response = api_instance.stop_job(job_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling JobsApi->stop_job: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **job_id** | [**str**](.md)|  | 

### Return type

[**Job**](Job.md)

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

