# coding: utf-8

"""
    osparc.io web API

    osparc-simcore public web API specifications  # noqa: E501

    The version of the OpenAPI document: 0.3.0
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest

import osparc
from osparc.api.meta_api import MetaApi  # noqa: E501
from osparc.rest import ApiException


class TestMetaApi(unittest.TestCase):
    """MetaApi unit test stubs"""

    def setUp(self):
        self.api = osparc.api.meta_api.MetaApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_get_service_metadata(self):
        """Test case for get_service_metadata

        Get Service Metadata  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
