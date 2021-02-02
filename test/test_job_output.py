# coding: utf-8

"""
    osparc public web api

    
    The version of the OpenAPI document: 0.4.0
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import osparc
from osparc.models.job_output import JobOutput  # noqa: E501
from osparc.rest import ApiException

class TestJobOutput(unittest.TestCase):
    """JobOutput unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test JobOutput
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = osparc.models.job_output.JobOutput()  # noqa: E501
        if include_optional :
            return JobOutput(
                name = 'SAR', 
                type = 'data:application/hdf5', 
                title = 'SAR field output file-id', 
                value = '1dc2b1e6-a139-47ad-9e0c-b7b791cd4d7a', 
                job_id = '9d9ac65-9f10-4e2f-a433-b5e412bb037b'
            )
        else :
            return JobOutput(
                name = 'SAR',
                value = '1dc2b1e6-a139-47ad-9e0c-b7b791cd4d7a',
                job_id = '9d9ac65-9f10-4e2f-a433-b5e412bb037b',
        )

    def testJobOutput(self):
        """Test JobOutput"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
