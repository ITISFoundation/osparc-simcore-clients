# coding: utf-8

"""
    osparc.io web API

    osparc-simcore public web API specifications  # noqa: E501

    The version of the OpenAPI document: 0.3.0
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import osparc
from osparc.models.job_inputs import JobInputs  # noqa: E501
from osparc.rest import ApiException


class TestJobInputs(unittest.TestCase):
    """JobInputs unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test JobInputs
        include_option is a boolean, when False only required
        params are included, when True both required and
        optional params are included"""
        # model = osparc.models.job_inputs.JobInputs()  # noqa: E501
        if include_optional:
            return JobInputs(values={"key": 33})
        else:
            return JobInputs(
                values={"key": 34},
            )

    def testJobInputs(self):
        """Test JobInputs"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == "__main__":
    unittest.main()