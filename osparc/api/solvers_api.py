# coding: utf-8

"""
    osparc public web api

    
    The version of the OpenAPI document: 0.4.0
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from osparc.api_client import ApiClient
from osparc.exceptions import (
    ApiTypeError,
    ApiValueError
)


class SolversApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def create_job(self, solver_id, **kwargs):  # noqa: E501
        """Create Job  # noqa: E501

        Creates a job for a solver with given inputs.  NOTE: This operation does **not** start the job  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_job(solver_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str solver_id: (required)
        :param list[JobInput] job_input:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Job
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.create_job_with_http_info(solver_id, **kwargs)  # noqa: E501

    def create_job_with_http_info(self, solver_id, **kwargs):  # noqa: E501
        """Create Job  # noqa: E501

        Creates a job for a solver with given inputs.  NOTE: This operation does **not** start the job  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_job_with_http_info(solver_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str solver_id: (required)
        :param list[JobInput] job_input:
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(Job, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['solver_id', 'job_input']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method create_job" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'solver_id' is set
        if self.api_client.client_side_validation and ('solver_id' not in local_var_params or  # noqa: E501
                                                        local_var_params['solver_id'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `solver_id` when calling `create_job`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'solver_id' in local_var_params:
            path_params['solver_id'] = local_var_params['solver_id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'job_input' in local_var_params:
            body_params = local_var_params['job_input']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/v0/solvers/{solver_id}/jobs', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Job',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_solver(self, solver_id, **kwargs):  # noqa: E501
        """Get Solver  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_solver(solver_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str solver_id: (required)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Solver
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.get_solver_with_http_info(solver_id, **kwargs)  # noqa: E501

    def get_solver_with_http_info(self, solver_id, **kwargs):  # noqa: E501
        """Get Solver  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_solver_with_http_info(solver_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str solver_id: (required)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(Solver, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['solver_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_solver" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'solver_id' is set
        if self.api_client.client_side_validation and ('solver_id' not in local_var_params or  # noqa: E501
                                                        local_var_params['solver_id'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `solver_id` when calling `get_solver`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'solver_id' in local_var_params:
            path_params['solver_id'] = local_var_params['solver_id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['HTTPBasic']  # noqa: E501

        return self.api_client.call_api(
            '/v0/solvers/{solver_id}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Solver',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_solver_by_name_and_version(self, solver_name, version, **kwargs):  # noqa: E501
        """Get Solver By Name And Version  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_solver_by_name_and_version(solver_name, version, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str solver_name: (required)
        :param str version: (required)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Solver
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.get_solver_by_name_and_version_with_http_info(solver_name, version, **kwargs)  # noqa: E501

    def get_solver_by_name_and_version_with_http_info(self, solver_name, version, **kwargs):  # noqa: E501
        """Get Solver By Name And Version  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_solver_by_name_and_version_with_http_info(solver_name, version, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str solver_name: (required)
        :param str version: (required)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(Solver, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['solver_name', 'version']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_solver_by_name_and_version" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'solver_name' is set
        if self.api_client.client_side_validation and ('solver_name' not in local_var_params or  # noqa: E501
                                                        local_var_params['solver_name'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `solver_name` when calling `get_solver_by_name_and_version`")  # noqa: E501
        # verify the required parameter 'version' is set
        if self.api_client.client_side_validation and ('version' not in local_var_params or  # noqa: E501
                                                        local_var_params['version'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `version` when calling `get_solver_by_name_and_version`")  # noqa: E501

        if self.api_client.client_side_validation and 'solver_name' in local_var_params and not re.search(r'^(simcore)\/(services)\/comp(\/[\w\/-]+)+$', local_var_params['solver_name']):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `solver_name` when calling `get_solver_by_name_and_version`, must conform to the pattern `/^(simcore)\/(services)\/comp(\/[\w\/-]+)+$/`")  # noqa: E501
        collection_formats = {}

        path_params = {}
        if 'solver_name' in local_var_params:
            path_params['solver_name'] = local_var_params['solver_name']  # noqa: E501
        if 'version' in local_var_params:
            path_params['version'] = local_var_params['version']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['HTTPBasic']  # noqa: E501

        return self.api_client.call_api(
            '/v0/solvers/{solver_name}/{version}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Solver',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def list_jobs(self, solver_id, **kwargs):  # noqa: E501
        """List Jobs  # noqa: E501

        List of all jobs with a given solver   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_jobs(solver_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str solver_id: (required)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: list[Job]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.list_jobs_with_http_info(solver_id, **kwargs)  # noqa: E501

    def list_jobs_with_http_info(self, solver_id, **kwargs):  # noqa: E501
        """List Jobs  # noqa: E501

        List of all jobs with a given solver   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_jobs_with_http_info(solver_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str solver_id: (required)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(list[Job], status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['solver_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list_jobs" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'solver_id' is set
        if self.api_client.client_side_validation and ('solver_id' not in local_var_params or  # noqa: E501
                                                        local_var_params['solver_id'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `solver_id` when calling `list_jobs`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'solver_id' in local_var_params:
            path_params['solver_id'] = local_var_params['solver_id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/v0/solvers/{solver_id}/jobs', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[Job]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def list_solvers(self, **kwargs):  # noqa: E501
        """List Solvers  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_solvers(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: list[Solver]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.list_solvers_with_http_info(**kwargs)  # noqa: E501

    def list_solvers_with_http_info(self, **kwargs):  # noqa: E501
        """List Solvers  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_solvers_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(list[Solver], status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = []  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list_solvers" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['HTTPBasic']  # noqa: E501

        return self.api_client.call_api(
            '/v0/solvers', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[Solver]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)
