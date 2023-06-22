# osparc.SolversApi

All URIs are relative to *https://api.osparc.io*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_job**](SolversApi.md#create_job) | **POST** /v0/solvers/{solver_key}/releases/{version}/jobs | Create Job
[**get_job**](SolversApi.md#get_job) | **GET** /v0/solvers/{solver_key}/releases/{version}/jobs/{job_id} | Get Job
[**get_job_output_logfile**](SolversApi.md#get_job_output_logfile) | **GET** /v0/solvers/{solver_key}/releases/{version}/jobs/{job_id}/outputs/logfile | Get Job Output Logfile
[**get_job_outputs**](SolversApi.md#get_job_outputs) | **GET** /v0/solvers/{solver_key}/releases/{version}/jobs/{job_id}/outputs | Get Job Outputs
[**get_solver**](SolversApi.md#get_solver) | **GET** /v0/solvers/{solver_key}/latest | Get Latest Release of a Solver
[**get_solver_release**](SolversApi.md#get_solver_release) | **GET** /v0/solvers/{solver_key}/releases/{version} | Get Solver Release
[**inspect_job**](SolversApi.md#inspect_job) | **POST** /v0/solvers/{solver_key}/releases/{version}/jobs/{job_id}:inspect | Inspect Job
[**list_jobs**](SolversApi.md#list_jobs) | **GET** /v0/solvers/{solver_key}/releases/{version}/jobs | List Jobs
[**list_solver_releases**](SolversApi.md#list_solver_releases) | **GET** /v0/solvers/{solver_key}/releases | List Solver Releases
[**list_solvers**](SolversApi.md#list_solvers) | **GET** /v0/solvers | List Solvers
[**list_solvers_releases**](SolversApi.md#list_solvers_releases) | **GET** /v0/solvers/releases | Lists All Releases
[**start_job**](SolversApi.md#start_job) | **POST** /v0/solvers/{solver_key}/releases/{version}/jobs/{job_id}:start | Start Job
[**stop_job**](SolversApi.md#stop_job) | **POST** /v0/solvers/{solver_key}/releases/{version}/jobs/{job_id}:stop | Stop Job


# **create_job**
> Job create_job(solver_key, version, job_inputs)

Create Job

Creates a job in a specific release with given inputs.  NOTE: This operation does **not** start the job

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

# Enter a context with an instance of the API client
with osparc.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = osparc.SolversApi(api_client)
    solver_key = 'solver_key_example' # str |
version = 'version_example' # str |
job_inputs = osparc.JobInputs() # JobInputs |

    try:
        # Create Job
        api_response = api_instance.create_job(solver_key, version, job_inputs)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling SolversApi->create_job: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **solver_key** | **str**|  |
 **version** | **str**|  |
 **job_inputs** | [**JobInputs**](JobInputs.md)|  |

### Return type

[**Job**](Job.md)

### Authorization

[HTTPBasic](../README.md#HTTPBasic)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API Classes]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_job**
> Job get_job(solver_key, version, job_id)

Get Job

Gets job of a given solver

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

# Enter a context with an instance of the API client
with osparc.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = osparc.SolversApi(api_client)
    solver_key = 'solver_key_example' # str |
version = 'version_example' # str |
job_id = 'job_id_example' # str |

    try:
        # Get Job
        api_response = api_instance.get_job(solver_key, version, job_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling SolversApi->get_job: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **solver_key** | **str**|  |
 **version** | **str**|  |
 **job_id** | [**str**](.md)|  |

### Return type

[**Job**](Job.md)

### Authorization

[HTTPBasic](../README.md#HTTPBasic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API Classes]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_job_output_logfile**
> file get_job_output_logfile(solver_key, version, job_id)

Get Job Output Logfile

Special extra output with persistent logs file for the solver run.  NOTE: this is not a log stream but a predefined output that is only available after the job is done.

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

# Enter a context with an instance of the API client
with osparc.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = osparc.SolversApi(api_client)
    solver_key = 'solver_key_example' # str |
version = 'version_example' # str |
job_id = 'job_id_example' # str |

    try:
        # Get Job Output Logfile
        api_response = api_instance.get_job_output_logfile(solver_key, version, job_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling SolversApi->get_job_output_logfile: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **solver_key** | **str**|  |
 **version** | **str**|  |
 **job_id** | [**str**](.md)|  |

### Return type

**file**

### Authorization

[HTTPBasic](../README.md#HTTPBasic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/octet-stream, application/zip, text/plain, application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**307** | Successful Response |  -  |
**200** | Returns a log file |  -  |
**404** | Log not found |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API Classes]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_job_outputs**
> JobOutputs get_job_outputs(solver_key, version, job_id)

Get Job Outputs

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

# Enter a context with an instance of the API client
with osparc.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = osparc.SolversApi(api_client)
    solver_key = 'solver_key_example' # str |
version = 'version_example' # str |
job_id = 'job_id_example' # str |

    try:
        # Get Job Outputs
        api_response = api_instance.get_job_outputs(solver_key, version, job_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling SolversApi->get_job_outputs: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **solver_key** | **str**|  |
 **version** | **str**|  |
 **job_id** | [**str**](.md)|  |

### Return type

[**JobOutputs**](JobOutputs.md)

### Authorization

[HTTPBasic](../README.md#HTTPBasic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API Classes]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_solver**
> Solver get_solver(solver_key)

Get Latest Release of a Solver

Gets latest release of a solver

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

# Enter a context with an instance of the API client
with osparc.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = osparc.SolversApi(api_client)
    solver_key = 'solver_key_example' # str |

    try:
        # Get Latest Release of a Solver
        api_response = api_instance.get_solver(solver_key)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling SolversApi->get_solver: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **solver_key** | **str**|  |

### Return type

[**Solver**](Solver.md)

### Authorization

[HTTPBasic](../README.md#HTTPBasic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API Classes]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_solver_release**
> Solver get_solver_release(solver_key, version)

Get Solver Release

Gets a specific release of a solver

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

# Enter a context with an instance of the API client
with osparc.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = osparc.SolversApi(api_client)
    solver_key = 'solver_key_example' # str |
version = 'version_example' # str |

    try:
        # Get Solver Release
        api_response = api_instance.get_solver_release(solver_key, version)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling SolversApi->get_solver_release: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **solver_key** | **str**|  |
 **version** | **str**|  |

### Return type

[**Solver**](Solver.md)

### Authorization

[HTTPBasic](../README.md#HTTPBasic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API Classes]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **inspect_job**
> JobStatus inspect_job(solver_key, version, job_id)

Inspect Job

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

# Enter a context with an instance of the API client
with osparc.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = osparc.SolversApi(api_client)
    solver_key = 'solver_key_example' # str |
version = 'version_example' # str |
job_id = 'job_id_example' # str |

    try:
        # Inspect Job
        api_response = api_instance.inspect_job(solver_key, version, job_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling SolversApi->inspect_job: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **solver_key** | **str**|  |
 **version** | **str**|  |
 **job_id** | [**str**](.md)|  |

### Return type

[**JobStatus**](JobStatus.md)

### Authorization

[HTTPBasic](../README.md#HTTPBasic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API Classes]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_jobs**
> list[Job] list_jobs(solver_key, version)

List Jobs

List of all jobs in a specific released solver

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

# Enter a context with an instance of the API client
with osparc.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = osparc.SolversApi(api_client)
    solver_key = 'solver_key_example' # str |
version = 'version_example' # str |

    try:
        # List Jobs
        api_response = api_instance.list_jobs(solver_key, version)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling SolversApi->list_jobs: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **solver_key** | **str**|  |
 **version** | **str**|  |

### Return type

[**list[Job]**](Job.md)

### Authorization

[HTTPBasic](../README.md#HTTPBasic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API Classes]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_solver_releases**
> list[Solver] list_solver_releases(solver_key)

List Solver Releases

Lists all releases of a given solver

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

# Enter a context with an instance of the API client
with osparc.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = osparc.SolversApi(api_client)
    solver_key = 'solver_key_example' # str |

    try:
        # List Solver Releases
        api_response = api_instance.list_solver_releases(solver_key)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling SolversApi->list_solver_releases: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **solver_key** | **str**|  |

### Return type

[**list[Solver]**](Solver.md)

### Authorization

[HTTPBasic](../README.md#HTTPBasic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API Classes]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_solvers**
> list[Solver] list_solvers()

List Solvers

Lists all available solvers (latest version)

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

# Enter a context with an instance of the API client
with osparc.ApiClient(configuration) as api_client:
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

[HTTPBasic](../README.md#HTTPBasic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API Classes]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_solvers_releases**
> list[Solver] list_solvers_releases()

Lists All Releases

Lists all released solvers (all released versions)

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

# Enter a context with an instance of the API client
with osparc.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = osparc.SolversApi(api_client)

    try:
        # Lists All Releases
        api_response = api_instance.list_solvers_releases()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling SolversApi->list_solvers_releases: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[Solver]**](Solver.md)

### Authorization

[HTTPBasic](../README.md#HTTPBasic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API Classes]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **start_job**
> JobStatus start_job(solver_key, version, job_id)

Start Job

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

# Enter a context with an instance of the API client
with osparc.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = osparc.SolversApi(api_client)
    solver_key = 'solver_key_example' # str |
version = 'version_example' # str |
job_id = 'job_id_example' # str |

    try:
        # Start Job
        api_response = api_instance.start_job(solver_key, version, job_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling SolversApi->start_job: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **solver_key** | **str**|  |
 **version** | **str**|  |
 **job_id** | [**str**](.md)|  |

### Return type

[**JobStatus**](JobStatus.md)

### Authorization

[HTTPBasic](../README.md#HTTPBasic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API Classes]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **stop_job**
> Job stop_job(solver_key, version, job_id)

Stop Job

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

# Enter a context with an instance of the API client
with osparc.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = osparc.SolversApi(api_client)
    solver_key = 'solver_key_example' # str |
version = 'version_example' # str |
job_id = 'job_id_example' # str |

    try:
        # Stop Job
        api_response = api_instance.stop_job(solver_key, version, job_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling SolversApi->stop_job: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **solver_key** | **str**|  |
 **version** | **str**|  |
 **job_id** | [**str**](.md)|  |

### Return type

[**Job**](Job.md)

### Authorization

[HTTPBasic](../README.md#HTTPBasic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API Classes]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

[Download as SolversApi.ipynb](clients/python/docs/auto_generated_docs/code_samples/SolversApi.ipynb ":ignore title")
