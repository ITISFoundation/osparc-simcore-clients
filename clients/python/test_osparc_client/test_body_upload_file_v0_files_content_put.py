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
from osparc import BodyUploadFileV0FilesContentPut  # noqa: E501
from osparc import ApiException

class TestBodyUploadFileV0FilesContentPut(unittest.TestCase):
    """BodyUploadFileV0FilesContentPut unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test BodyUploadFileV0FilesContentPut
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = osparc.models.body_upload_file_v0_files_content_put.BodyUploadFileV0FilesContentPut()  # noqa: E501
        if include_optional :
            return BodyUploadFileV0FilesContentPut(
                file = bytes(b'blah')
            )
        else :
            return BodyUploadFileV0FilesContentPut(
                file = bytes(b'blah'),
        )

    def testBodyUploadFileV0FilesContentPut(self):
        """Test BodyUploadFileV0FilesContentPut"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
