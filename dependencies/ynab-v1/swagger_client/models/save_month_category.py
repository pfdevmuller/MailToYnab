# coding: utf-8

"""
    YNAB API Endpoints

    Our API uses a REST based design, leverages the JSON data format, and relies upon HTTPS for transport. We respond with meaningful HTTP response codes and if an error occurs, we include error details in the response body.  API Documentation is at https://api.youneedabudget.com  # noqa: E501

    OpenAPI spec version: 1.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six


class SaveMonthCategory(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'budgeted': 'int'
    }

    attribute_map = {
        'budgeted': 'budgeted'
    }

    def __init__(self, budgeted=None):  # noqa: E501
        """SaveMonthCategory - a model defined in Swagger"""  # noqa: E501
        self._budgeted = None
        self.discriminator = None
        self.budgeted = budgeted

    @property
    def budgeted(self):
        """Gets the budgeted of this SaveMonthCategory.  # noqa: E501

        Budgeted amount in milliunits format  # noqa: E501

        :return: The budgeted of this SaveMonthCategory.  # noqa: E501
        :rtype: int
        """
        return self._budgeted

    @budgeted.setter
    def budgeted(self, budgeted):
        """Sets the budgeted of this SaveMonthCategory.

        Budgeted amount in milliunits format  # noqa: E501

        :param budgeted: The budgeted of this SaveMonthCategory.  # noqa: E501
        :type: int
        """
        if budgeted is None:
            raise ValueError("Invalid value for `budgeted`, must not be `None`")  # noqa: E501

        self._budgeted = budgeted

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
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
        if issubclass(SaveMonthCategory, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, SaveMonthCategory):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
