# coding: utf-8

"""
    osparc.io web API

    osparc-simcore public web API specifications  # noqa: E501

    The version of the OpenAPI document: 0.4.0
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest

from osparc import File  # noqa: E501


class TestFile(unittest.TestCase):
    """File unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test File
        include_option is a boolean, when False only required
        params are included, when True both required and
        optional params are included"""
        # model = osparc.models.file.File()  # noqa: E501
        if include_optional:
            return File(id="0", filename="0", content_type="0", checksum="0")
        else:
            return File(
                id="0",
                filename="0",
                checksum="333daca44bef79b1af3126bb4925bca5c86e7de27f69679913104b9f6d1a40fb",
            )

    def testFile(self):
        """Test File"""
        self.make_instance(include_optional=False)
        self.make_instance(include_optional=True)


if __name__ == "__main__":
    unittest.main()
