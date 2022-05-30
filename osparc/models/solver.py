# coding: utf-8

"""
    osparc.io web API

    osparc-simcore public web API specifications  # noqa: E501

    The version of the OpenAPI document: 0.4.0
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from osparc.configuration import Configuration


class Solver(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'id': 'str',
        'version': 'str',
        'title': 'str',
        'description': 'str',
        'maintainer': 'str',
        'url': 'str'
    }

    attribute_map = {
        'id': 'id',
        'version': 'version',
        'title': 'title',
        'description': 'description',
        'maintainer': 'maintainer',
        'url': 'url'
    }

    def __init__(self, id=None, version=None, title=None, description=None, maintainer=None, url=None, local_vars_configuration=None):  # noqa: E501
        """Solver - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._version = None
        self._title = None
        self._description = None
        self._maintainer = None
        self._url = None
        self.discriminator = None

        self.id = id
        self.version = version
        self.title = title
        if description is not None:
            self.description = description
        self.maintainer = maintainer
        self.url = url

    @property
    def id(self):
        """Gets the id of this Solver.  # noqa: E501

        Solver identifier  # noqa: E501

        :return: The id of this Solver.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Solver.

        Solver identifier  # noqa: E501

        :param id: The id of this Solver.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and id is None:  # noqa: E501
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                id is not None and not re.search(r'^(simcore)\/(services)\/comp(\/[\w\/-]+)+$', id)):  # noqa: E501
            raise ValueError(r"Invalid value for `id`, must be a follow pattern or equal to `/^(simcore)\/(services)\/comp(\/[\w\/-]+)+$/`")  # noqa: E501

        self._id = id

    @property
    def version(self):
        """Gets the version of this Solver.  # noqa: E501

        semantic version number of the node  # noqa: E501

        :return: The version of this Solver.  # noqa: E501
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this Solver.

        semantic version number of the node  # noqa: E501

        :param version: The version of this Solver.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and version is None:  # noqa: E501
            raise ValueError("Invalid value for `version`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                version is not None and not re.search(r'^(0|[1-9]\d*)(\.(0|[1-9]\d*)){2}(-(0|[1-9]\d*|\d*[-a-zA-Z][-\da-zA-Z]*)(\.(0|[1-9]\d*|\d*[-a-zA-Z][-\da-zA-Z]*))*)?(\+[-\da-zA-Z]+(\.[-\da-zA-Z-]+)*)?$', version)):  # noqa: E501
            raise ValueError(r"Invalid value for `version`, must be a follow pattern or equal to `/^(0|[1-9]\d*)(\.(0|[1-9]\d*)){2}(-(0|[1-9]\d*|\d*[-a-zA-Z][-\da-zA-Z]*)(\.(0|[1-9]\d*|\d*[-a-zA-Z][-\da-zA-Z]*))*)?(\+[-\da-zA-Z]+(\.[-\da-zA-Z-]+)*)?$/`")  # noqa: E501

        self._version = version

    @property
    def title(self):
        """Gets the title of this Solver.  # noqa: E501

        Human readable name  # noqa: E501

        :return: The title of this Solver.  # noqa: E501
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """Sets the title of this Solver.

        Human readable name  # noqa: E501

        :param title: The title of this Solver.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and title is None:  # noqa: E501
            raise ValueError("Invalid value for `title`, must not be `None`")  # noqa: E501

        self._title = title

    @property
    def description(self):
        """Gets the description of this Solver.  # noqa: E501


        :return: The description of this Solver.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this Solver.


        :param description: The description of this Solver.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def maintainer(self):
        """Gets the maintainer of this Solver.  # noqa: E501


        :return: The maintainer of this Solver.  # noqa: E501
        :rtype: str
        """
        return self._maintainer

    @maintainer.setter
    def maintainer(self, maintainer):
        """Sets the maintainer of this Solver.


        :param maintainer: The maintainer of this Solver.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and maintainer is None:  # noqa: E501
            raise ValueError("Invalid value for `maintainer`, must not be `None`")  # noqa: E501

        self._maintainer = maintainer

    @property
    def url(self):
        """Gets the url of this Solver.  # noqa: E501

        Link to get this resource  # noqa: E501

        :return: The url of this Solver.  # noqa: E501
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url):
        """Sets the url of this Solver.

        Link to get this resource  # noqa: E501

        :param url: The url of this Solver.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and url is None:  # noqa: E501
            raise ValueError("Invalid value for `url`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                url is not None and len(url) > 2083):
            raise ValueError("Invalid value for `url`, length must be less than or equal to `2083`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                url is not None and len(url) < 1):
            raise ValueError("Invalid value for `url`, length must be greater than or equal to `1`")  # noqa: E501

        self._url = url

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, Solver):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Solver):
            return True

        return self.to_dict() != other.to_dict()
