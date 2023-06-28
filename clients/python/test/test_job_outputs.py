# coding: utf-8

"""
    osparc.io web API

    osparc-simcore public web API specifications  # noqa: E501

    The version of the OpenAPI document: 0.4.0
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import osparc
from osparc.models.job_outputs import JobOutputs  # noqa: E501
from osparc.exceptions import ApiException

class TestJobOutputs(unittest.TestCase):
    """JobOutputs unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test JobOutputs
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = osparc.models.job_outputs.JobOutputs()  # noqa: E501
        if include_optional :
            return JobOutputs(
                job_id = '0',
                results = {
                    'key' : 3.14
                    }
            )
        else :
            return JobOutputs(
                job_id = '0',
                results = {
                    'key' : 42
                    },
        )

    def testJobOutputs(self):
        """Test JobOutputs"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
