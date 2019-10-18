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
from swagger_client.models.category import Category  # noqa: F401,E501
from swagger_client.models.category_group import CategoryGroup  # noqa: F401,E501


class CategoryGroupWithCategories(CategoryGroup):
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
        'categories': 'list[Category]'
    }
    if hasattr(CategoryGroup, "swagger_types"):
        swagger_types.update(CategoryGroup.swagger_types)

    attribute_map = {
        'categories': 'categories'
    }
    if hasattr(CategoryGroup, "attribute_map"):
        attribute_map.update(CategoryGroup.attribute_map)

    def __init__(self, categories=None, *args, **kwargs):  # noqa: E501
        """CategoryGroupWithCategories - a model defined in Swagger"""  # noqa: E501
        self._categories = None
        self.discriminator = None
        self.categories = categories
        CategoryGroup.__init__(self, *args, **kwargs)

    @property
    def categories(self):
        """Gets the categories of this CategoryGroupWithCategories.  # noqa: E501

        Category group categories.  Amounts (budgeted, activity, balance, etc.) are specific to the current budget month (UTC).  # noqa: E501

        :return: The categories of this CategoryGroupWithCategories.  # noqa: E501
        :rtype: list[Category]
        """
        return self._categories

    @categories.setter
    def categories(self, categories):
        """Sets the categories of this CategoryGroupWithCategories.

        Category group categories.  Amounts (budgeted, activity, balance, etc.) are specific to the current budget month (UTC).  # noqa: E501

        :param categories: The categories of this CategoryGroupWithCategories.  # noqa: E501
        :type: list[Category]
        """
        if categories is None:
            raise ValueError("Invalid value for `categories`, must not be `None`")  # noqa: E501

        self._categories = categories

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
        if issubclass(CategoryGroupWithCategories, dict):
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
        if not isinstance(other, CategoryGroupWithCategories):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
