# coding: utf-8

"""
    osparc.io web API

    osparc-simcore public web API specifications  # noqa: E501

    The version of the OpenAPI document: 0.4.0
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest

from osparc import ApiClient, Configuration, UsersApi  # noqa: E501


class TestUsersApi(unittest.TestCase):
    """UsersApi unit test stubs"""

    def setUp(self):
        self.api = UsersApi(
            api_client=ApiClient(configuration=Configuration())
        )  # noqa: E501

    def tearDown(self):
        pass

    def test_get_my_profile(self):
        """Test case for get_my_profile

        Get My Profile  # noqa: E501
        """
        pass

    def test_update_my_profile(self):
        """Test case for update_my_profile

        Update My Profile  # noqa: E501
        """
        pass


if __name__ == "__main__":
    unittest.main()
