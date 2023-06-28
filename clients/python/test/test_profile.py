# coding: utf-8

"""
    osparc_client.io web API

    osparc_client-simcore public web API specifications  # noqa: E501

    The version of the OpenAPI document: 0.4.0
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import osparc_client
from osparc_client.models.profile import Profile  # noqa: E501
from osparc_client.exceptions import ApiException

class TestProfile(unittest.TestCase):
    """Profile unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test Profile
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = osparc_client.models.profile.Profile()  # noqa: E501
        if include_optional :
            return Profile(
                first_name = 'James',
                last_name = 'Maxwell',
                login = '0',
                role = 'ANONYMOUS',
                groups = osparc_client.models.groups.Groups(
                    me = osparc_client.models.users_group.UsersGroup(
                        gid = '0',
                        label = '0',
                        description = '0', ),
                    organizations = [
                        osparc_client.models.users_group.UsersGroup(
                            gid = '0',
                            label = '0',
                            description = '0', )
                        ],
                    all = osparc_client.models.users_group.UsersGroup(
                        gid = '0',
                        label = '0',
                        description = '0', ), ),
                gravatar_id = '0'
            )
        else :
            return Profile(
                login = '0',
                role = 'ANONYMOUS',
        )

    def testProfile(self):
        """Test Profile"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
