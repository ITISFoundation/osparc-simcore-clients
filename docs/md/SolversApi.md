# osparc.SolversApi

All URIs are relative to *https://api.osparc.io*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_job**](SolversApi.md#create_job) | **POST** /v0/solvers/{solver_id}/jobs | Create Job
[**get_solver**](SolversApi.md#get_solver) | **GET** /v0/solvers/{solver_id} | Get Solver
[**get_solver_by_name_and_version**](SolversApi.md#get_solver_by_name_and_version) | **GET** /v0/solvers/{solver_name}/{version} | Get Solver By Name And Version
[**list_jobs**](SolversApi.md#list_jobs) | **GET** /v0/solvers/{solver_id}/jobs | List Jobs
[**list_solvers**](SolversApi.md#list_solvers) | **GET** /v0/solvers | List Solvers


# **create_job**
> Job create_job(solver_id, job_input=job_input)

Create Job

Creates a job for a solver with given inputs.  NOTE: This operation does **not** start the job

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
    api_instance = osparc.SolversApi(api_client)
    solver_id = 'solver_id_example' # str | 
job_input = [osparc.JobInput()] # list[JobInput] |  (optional)

    try:
        # Create Job
        api_response = api_instance.create_job(solver_id, job_input=job_input)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling SolversApi->create_job: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **solver_id** | [**str**](.md)|  | 
 **job_input** | [**list[JobInput]**](JobInput.md)|  | [optional] 

### Return type

[**Job**](Job.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_solver**
> Solver get_solver(solver_id)

Get Solver

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
    api_instance = osparc.SolversApi(api_client)
    solver_id = 'solver_id_example' # str | 

    try:
        # Get Solver
        api_response = api_instance.get_solver(solver_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling SolversApi->get_solver: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **solver_id** | [**str**](.md)|  | 

### Return type

[**Solver**](Solver.md)

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

# **get_solver_by_name_and_version**
> Solver get_solver_by_name_and_version(solver_name, version)

Get Solver By Name And Version

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
    api_instance = osparc.SolversApi(api_client)
    solver_name = 'solver_name_example' # str | 
version = 'version_example' # str | 

    try:
        # Get Solver By Name And Version
        api_response = api_instance.get_solver_by_name_and_version(solver_name, version)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling SolversApi->get_solver_by_name_and_version: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **solver_name** | **str**|  | 
 **version** | **str**|  | 

### Return type

[**Solver**](Solver.md)

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

# **list_jobs**
> list[Job] list_jobs(solver_id)

List Jobs

List of all jobs with a given solver 

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
    api_instance = osparc.SolversApi(api_client)
    solver_id = 'solver_id_example' # str | 

    try:
        # List Jobs
        api_response = api_instance.list_jobs(solver_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling SolversApi->list_jobs: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **solver_id** | [**str**](.md)|  | 

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
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_solvers**
> list[Solver] list_solvers()

List Solvers

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
    api_instance = osparc.SolversApi(api_client)
    
    try:
        # List Solvers
        api_response = api_instance.list_solvers()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling SolversApi->list_solvers: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[Solver]**](Solver.md)

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

