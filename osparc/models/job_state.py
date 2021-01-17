# coding: utf-8

"""
    Public API Server

    **osparc-simcore Public RESTful API Specifications** ## Python Library - Check the [documentation](https://itisfoundation.github.io/osparc-simcore-python-client) - Quick install: ``pip install git+https://github.com/ITISFoundation/osparc-simcore-python-client.git``   # noqa: E501

    The version of the OpenAPI document: 0.4.0
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from osparc.configuration import Configuration


class JobState(object):
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
        'status': 'TaskStates',
        'progress': 'float',
        'submitted_at': 'datetime',
        'started_at': 'datetime',
        'stopped_at': 'datetime'
    }

    attribute_map = {
        'status': 'status',
        'progress': 'progress',
        'submitted_at': 'submitted_at',
        'started_at': 'started_at',
        'stopped_at': 'stopped_at'
    }

    def __init__(self, status=None, progress=None, submitted_at=None, started_at=None, stopped_at=None, local_vars_configuration=None):  # noqa: E501
        """JobState - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._status = None
        self._progress = None
        self._submitted_at = None
        self._started_at = None
        self._stopped_at = None
        self.discriminator = None

        self.status = status
        self.progress = progress
        self.submitted_at = submitted_at
        self.started_at = started_at
        if stopped_at is not None:
            self.stopped_at = stopped_at

    @property
    def status(self):
        """Gets the status of this JobState.  # noqa: E501


        :return: The status of this JobState.  # noqa: E501
        :rtype: TaskStates
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this JobState.


        :param status: The status of this JobState.  # noqa: E501
        :type: TaskStates
        """
        if self.local_vars_configuration.client_side_validation and status is None:  # noqa: E501
            raise ValueError("Invalid value for `status`, must not be `None`")  # noqa: E501

        self._status = status

    @property
    def progress(self):
        """Gets the progress of this JobState.  # noqa: E501


        :return: The progress of this JobState.  # noqa: E501
        :rtype: float
        """
        return self._progress

    @progress.setter
    def progress(self, progress):
        """Sets the progress of this JobState.


        :param progress: The progress of this JobState.  # noqa: E501
        :type: float
        """
        if self.local_vars_configuration.client_side_validation and progress is None:  # noqa: E501
            raise ValueError("Invalid value for `progress`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                progress is not None and progress > 100.0):  # noqa: E501
            raise ValueError("Invalid value for `progress`, must be a value less than or equal to `100.0`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                progress is not None and progress < 0.0):  # noqa: E501
            raise ValueError("Invalid value for `progress`, must be a value greater than or equal to `0.0`")  # noqa: E501

        self._progress = progress

    @property
    def submitted_at(self):
        """Gets the submitted_at of this JobState.  # noqa: E501


        :return: The submitted_at of this JobState.  # noqa: E501
        :rtype: datetime
        """
        return self._submitted_at

    @submitted_at.setter
    def submitted_at(self, submitted_at):
        """Sets the submitted_at of this JobState.


        :param submitted_at: The submitted_at of this JobState.  # noqa: E501
        :type: datetime
        """
        if self.local_vars_configuration.client_side_validation and submitted_at is None:  # noqa: E501
            raise ValueError("Invalid value for `submitted_at`, must not be `None`")  # noqa: E501

        self._submitted_at = submitted_at

    @property
    def started_at(self):
        """Gets the started_at of this JobState.  # noqa: E501


        :return: The started_at of this JobState.  # noqa: E501
        :rtype: datetime
        """
        return self._started_at

    @started_at.setter
    def started_at(self, started_at):
        """Sets the started_at of this JobState.


        :param started_at: The started_at of this JobState.  # noqa: E501
        :type: datetime
        """
        if self.local_vars_configuration.client_side_validation and started_at is None:  # noqa: E501
            raise ValueError("Invalid value for `started_at`, must not be `None`")  # noqa: E501

        self._started_at = started_at

    @property
    def stopped_at(self):
        """Gets the stopped_at of this JobState.  # noqa: E501


        :return: The stopped_at of this JobState.  # noqa: E501
        :rtype: datetime
        """
        return self._stopped_at

    @stopped_at.setter
    def stopped_at(self, stopped_at):
        """Sets the stopped_at of this JobState.


        :param stopped_at: The stopped_at of this JobState.  # noqa: E501
        :type: datetime
        """

        self._stopped_at = stopped_at

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
        if not isinstance(other, JobState):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, JobState):
            return True

        return self.to_dict() != other.to_dict()
