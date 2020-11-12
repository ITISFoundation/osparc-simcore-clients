# coding: utf-8

"""
    Public API Server

    **osparc-simcore Public RESTful API Specifications** ## Python Library - Check the [documentation](https://itisfoundation.github.io/osparc-simcore-python-client) - Quick install: ``pip install git+https://github.com/ITISFoundation/osparc-simcore-python-client.git``   # noqa: E501

    The version of the OpenAPI document: 0.4.0
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import osparc
from osparc.models.meta import Meta  # noqa: E501
from osparc.rest import ApiException

class TestMeta(unittest.TestCase):
    """Meta unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test Meta
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = osparc.models.meta.Meta()  # noqa: E501
        if include_optional :
            return Meta(
                name = 'simcore_service_foo"',
                version = '2.4.45',
                released = {
                       "v1": "1.3.4",
                        "v2": "2.4.45"
                    },
                docs_url = 'https://api.osparc.io/doc',
                docs_dev_url = 'https://api.osparc.io/dev/doc',
            )
        else :
            return Meta(
                name = 'simcore_service_foo"',
                version = '2.4.45',
                docs_url = 'https://api.osparc.io/doc',
                docs_dev_url = 'https://api.osparc.io/dev/doc',
        )

    def testMeta(self):
        """Test Meta"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
