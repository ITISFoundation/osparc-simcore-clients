# coding: utf-8

"""
    osparc.io web API

    osparc-simcore public web API specifications  # noqa: E501

    The version of the OpenAPI document: 0.3.0
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from osparc.configuration import Configuration


class JobStatus(object):
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
        'job_id': 'str',
        'state': 'TaskStates',
        'progress': 'int',
        'submitted_at': 'datetime',
        'started_at': 'datetime',
        'stopped_at': 'datetime'
    }

    attribute_map = {
        'job_id': 'job_id',
        'state': 'state',
        'progress': 'progress',
        'submitted_at': 'submitted_at',
        'started_at': 'started_at',
        'stopped_at': 'stopped_at'
    }

    def __init__(self, job_id=None, state=None, progress=0, submitted_at=None, started_at=None, stopped_at=None, local_vars_configuration=None):  # noqa: E501
        """JobStatus - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._job_id = None
        self._state = None
        self._progress = None
        self._submitted_at = None
        self._started_at = None
        self._stopped_at = None
        self.discriminator = None

        self.job_id = job_id
        self.state = state
        if progress is not None:
            self.progress = progress
        self.submitted_at = submitted_at
        if started_at is not None:
            self.started_at = started_at
        if stopped_at is not None:
            self.stopped_at = stopped_at

    @property
    def job_id(self):
        """Gets the job_id of this JobStatus.  # noqa: E501


        :return: The job_id of this JobStatus.  # noqa: E501
        :rtype: str
        """
        return self._job_id

    @job_id.setter
    def job_id(self, job_id):
        """Sets the job_id of this JobStatus.


        :param job_id: The job_id of this JobStatus.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and job_id is None:  # noqa: E501
            raise ValueError("Invalid value for `job_id`, must not be `None`")  # noqa: E501

        self._job_id = job_id

    @property
    def state(self):
        """Gets the state of this JobStatus.  # noqa: E501


        :return: The state of this JobStatus.  # noqa: E501
        :rtype: TaskStates
        """
        return self._state

    @state.setter
    def state(self, state):
        """Sets the state of this JobStatus.


        :param state: The state of this JobStatus.  # noqa: E501
        :type: TaskStates
        """
        if self.local_vars_configuration.client_side_validation and state is None:  # noqa: E501
            raise ValueError("Invalid value for `state`, must not be `None`")  # noqa: E501

        self._state = state

    @property
    def progress(self):
        """Gets the progress of this JobStatus.  # noqa: E501


        :return: The progress of this JobStatus.  # noqa: E501
        :rtype: int
        """
        return self._progress

    @progress.setter
    def progress(self, progress):
        """Sets the progress of this JobStatus.


        :param progress: The progress of this JobStatus.  # noqa: E501
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                progress is not None and progress > 100):  # noqa: E501
            raise ValueError("Invalid value for `progress`, must be a value less than or equal to `100`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                progress is not None and progress < 0):  # noqa: E501
            raise ValueError("Invalid value for `progress`, must be a value greater than or equal to `0`")  # noqa: E501

        self._progress = progress

    @property
    def submitted_at(self):
        """Gets the submitted_at of this JobStatus.  # noqa: E501


        :return: The submitted_at of this JobStatus.  # noqa: E501
        :rtype: datetime
        """
        return self._submitted_at

    @submitted_at.setter
    def submitted_at(self, submitted_at):
        """Sets the submitted_at of this JobStatus.


        :param submitted_at: The submitted_at of this JobStatus.  # noqa: E501
        :type: datetime
        """
        if self.local_vars_configuration.client_side_validation and submitted_at is None:  # noqa: E501
            raise ValueError("Invalid value for `submitted_at`, must not be `None`")  # noqa: E501

        self._submitted_at = submitted_at

    @property
    def started_at(self):
        """Gets the started_at of this JobStatus.  # noqa: E501

        Timestamp that indicate the moment the solver starts execution or None if the event did not occur  # noqa: E501

        :return: The started_at of this JobStatus.  # noqa: E501
        :rtype: datetime
        """
        return self._started_at

    @started_at.setter
    def started_at(self, started_at):
        """Sets the started_at of this JobStatus.

        Timestamp that indicate the moment the solver starts execution or None if the event did not occur  # noqa: E501

        :param started_at: The started_at of this JobStatus.  # noqa: E501
        :type: datetime
        """

        self._started_at = started_at

    @property
    def stopped_at(self):
        """Gets the stopped_at of this JobStatus.  # noqa: E501

        Timestamp at which the solver finished or killed execution or None if the event did not occur  # noqa: E501

        :return: The stopped_at of this JobStatus.  # noqa: E501
        :rtype: datetime
        """
        return self._stopped_at

    @stopped_at.setter
    def stopped_at(self, stopped_at):
        """Sets the stopped_at of this JobStatus.

        Timestamp at which the solver finished or killed execution or None if the event did not occur  # noqa: E501

        :param stopped_at: The stopped_at of this JobStatus.  # noqa: E501
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
        if not isinstance(other, JobStatus):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, JobStatus):
            return True

        return self.to_dict() != other.to_dict()
