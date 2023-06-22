# coding: utf-8

"""
    osparc.io web API

    osparc-simcore public web API specifications  # noqa: E501

    The version of the OpenAPI document: 0.4.0
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest

import osparc
from osparc.api.solvers_api import SolversApi  # noqa: E501
from osparc.rest import ApiException


class TestSolversApi(unittest.TestCase):
    """SolversApi unit test stubs"""

    def setUp(self):
        self.api = osparc.api.solvers_api.SolversApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_create_job(self):
        """Test case for create_job

        Create Job  # noqa: E501
        """
        pass

    def test_get_job(self):
        """Test case for get_job

        Get Job  # noqa: E501
        """
        pass

    def test_get_job_output_logfile(self):
        """Test case for get_job_output_logfile

        Get Job Output Logfile  # noqa: E501
        """
        pass

    def test_get_job_outputs(self):
        """Test case for get_job_outputs

        Get Job Outputs  # noqa: E501
        """
        pass

    def test_get_solver(self):
        """Test case for get_solver

        Get Latest Release of a Solver  # noqa: E501
        """
        pass

    def test_get_solver_release(self):
        """Test case for get_solver_release

        Get Solver Release  # noqa: E501
        """
        pass

    def test_inspect_job(self):
        """Test case for inspect_job

        Inspect Job  # noqa: E501
        """
        pass

    def test_list_jobs(self):
        """Test case for list_jobs

        List Jobs  # noqa: E501
        """
        pass

    def test_list_solver_releases(self):
        """Test case for list_solver_releases

        List Solver Releases  # noqa: E501
        """
        pass

    def test_list_solvers(self):
        """Test case for list_solvers

        List Solvers  # noqa: E501
        """
        pass

    def test_list_solvers_releases(self):
        """Test case for list_solvers_releases

        Lists All Releases  # noqa: E501
        """
        pass

    def test_start_job(self):
        """Test case for start_job

        Start Job  # noqa: E501
        """
        pass

    def test_stop_job(self):
        """Test case for stop_job

        Stop Job  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()