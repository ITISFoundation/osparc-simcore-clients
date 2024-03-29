# coding: utf-8

"""
    osparc.io web API

    osparc-simcore public web API specifications  # noqa: E501

    The version of the OpenAPI document: 0.4.0
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest

from osparc import Groups, UsersGroup  # noqa: E501


class TestGroups(unittest.TestCase):
    """Groups unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test Groups
        include_option is a boolean, when False only required
        params are included, when True both required and
        optional params are included"""
        # model = osparc.models.groups.Groups()  # noqa: E501
        if include_optional:
            return Groups(
                me=UsersGroup(
                    gid="0",
                    label="0",
                    description="0",
                ),
                organizations=[
                    UsersGroup(
                        gid="0",
                        label="0",
                        description="0",
                    )
                ],
                all=UsersGroup(
                    gid="0",
                    label="0",
                    description="0",
                ),
            )
        else:
            return Groups(
                me=UsersGroup(
                    gid="0",
                    label="0",
                    description="0",
                ),
                all=UsersGroup(
                    gid="0",
                    label="0",
                    description="0",
                ),
            )

    def testGroups(self):
        """Test Groups"""
        self.make_instance(include_optional=False)
        self.make_instance(include_optional=True)


if __name__ == "__main__":
    unittest.main()
