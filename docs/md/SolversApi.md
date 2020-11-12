# osparc.SolversApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_job**](SolversApi.md#create_job) | **POST** /v0/solvers/{solver_id}/jobs | Create Job
[**get_job**](SolversApi.md#get_job) | **GET** /v0/solvers/{solver_id}/jobs/{job_id} | Get Job
[**get_job_output**](SolversApi.md#get_job_output) | **GET** /v0/solvers/{solver_id}/jobs/{job_id}/outputs/{output_key} | Get Job Output
[**get_solver_by_id**](SolversApi.md#get_solver_by_id) | **GET** /v0/solvers/{solver_id} | Get Solver By Id
[**get_solver_by_name_and_version**](SolversApi.md#get_solver_by_name_and_version) | **GET** /v0/solvers/{solver_name}/{version} | Get Solver By Name And Version
[**inspect_job**](SolversApi.md#inspect_job) | **POST** /v0/solvers/{solver_id}/jobs/{job_id}:inspect | Inspect Job
[**list_job_outputs**](SolversApi.md#list_job_outputs) | **GET** /v0/solvers/{solver_id}/jobs/{job_id}/outputs | List Job Outputs
[**list_jobs**](SolversApi.md#list_jobs) | **GET** /v0/solvers/{solver_id}/jobs | List Jobs
[**list_solvers**](SolversApi.md#list_solvers) | **GET** /v0/solvers | List Solvers
[**run_job**](SolversApi.md#run_job) | **POST** /v0/solvers/{solver_id}/jobs/{job_id}:run | Run Job
[**start_job**](SolversApi.md#start_job) | **POST** /v0/solvers/{solver_id}/jobs/{job_id}:start | Start Job
[**stop_job**](SolversApi.md#stop_job) | **POST** /v0/solvers/{solver_id}/jobs/{job_id}:stop | Stop Job


# **create_job**
> Job create_job(solver_id, job_input=job_input)

Create Job

Jobs a solver with given inputs 

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

# **get_job**
> Job get_job(solver_id, job_id)

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
    api_instance = osparc.SolversApi(api_client)
    solver_id = 'solver_id_example' # str | 
job_id = 'job_id_example' # str | 

    try:
        # Get Job
        api_response = api_instance.get_job(solver_id, job_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling SolversApi->get_job: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **solver_id** | [**str**](.md)|  | 
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
> SolverOutput get_job_output(solver_id, job_id, output_key)

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
    api_instance = osparc.SolversApi(api_client)
    solver_id = 'solver_id_example' # str | 
job_id = 'job_id_example' # str | 
output_key = 'output_key_example' # str | 

    try:
        # Get Job Output
        api_response = api_instance.get_job_output(solver_id, job_id, output_key)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling SolversApi->get_job_output: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **solver_id** | [**str**](.md)|  | 
 **job_id** | [**str**](.md)|  | 
 **output_key** | **str**|  | 

### Return type

[**SolverOutput**](SolverOutput.md)

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

# **get_solver_by_id**
> Solver get_solver_by_id(solver_id)

Get Solver By Id

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
        # Get Solver By Id
        api_response = api_instance.get_solver_by_id(solver_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling SolversApi->get_solver_by_id: %s\n" % e)
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

# **inspect_job**
> JobState inspect_job(solver_id)

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
    api_instance = osparc.SolversApi(api_client)
    solver_id = 'solver_id_example' # str | 

    try:
        # Inspect Job
        api_response = api_instance.inspect_job(solver_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling SolversApi->inspect_job: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **solver_id** | [**str**](.md)|  | 

### Return type

[**JobState**](JobState.md)

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

# **list_job_outputs**
> list[JobOutput] list_job_outputs(solver_id, job_id)

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
    api_instance = osparc.SolversApi(api_client)
    solver_id = 'solver_id_example' # str | 
job_id = 'job_id_example' # str | 

    try:
        # List Job Outputs
        api_response = api_instance.list_job_outputs(solver_id, job_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling SolversApi->list_job_outputs: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **solver_id** | [**str**](.md)|  | 
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

# **list_jobs**
> object list_jobs(solver_id)

List Jobs

List of all jobs (could be finished) by user of a given solver 

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

# **list_solvers**
> list[Solver] list_solvers()

List Solvers

Returns a list of the latest version of each solver

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

# **run_job**
> Job run_job(solver_id, job_input=job_input)

Run Job

create + start job in a single call 

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
        # Run Job
        api_response = api_instance.run_job(solver_id, job_input=job_input)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling SolversApi->run_job: %s\n" % e)
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

# **start_job**
> Job start_job(solver_id, job_id)

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
    api_instance = osparc.SolversApi(api_client)
    solver_id = 'solver_id_example' # str | 
job_id = 'job_id_example' # str | 

    try:
        # Start Job
        api_response = api_instance.start_job(solver_id, job_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling SolversApi->start_job: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **solver_id** | [**str**](.md)|  | 
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

# **stop_job**
> Job stop_job(solver_id, job_id)

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
    api_instance = osparc.SolversApi(api_client)
    solver_id = 'solver_id_example' # str | 
job_id = 'job_id_example' # str | 

    try:
        # Stop Job
        api_response = api_instance.stop_job(solver_id, job_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling SolversApi->stop_job: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **solver_id** | [**str**](.md)|  | 
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

