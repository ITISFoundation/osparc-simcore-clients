# coding: utf-8

"""
    osparc.io web API

    osparc-simcore public web API specifications  # noqa: E501

    The version of the OpenAPI document: 0.3.0
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest

from osparc.models.file import File  # noqa: E501


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
            return File(
                id="f0e1fb11-208d-3ed2-b5ef-cab7a7398f78",
                filename="Architecture-of-Scalable-Distributed-ETL-System-whitepaper.pdf",
                content_type="application/pdf",
                checksum="de47d0e1229aa2dfb80097389094eadd-1",
            )
        else:
            return File(
                id="f0e1fb11-208d-3ed2-b5ef-cab7a7398f78",
                filename="Architecture-of-Scalable-Distributed-ETL-System-whitepaper.pdf",
            )

    def testFile(self):
        """Test File"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == "__main__":
    unittest.main()
