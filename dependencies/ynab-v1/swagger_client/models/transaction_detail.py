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
from swagger_client.models.sub_transaction import SubTransaction  # noqa: F401,E501
from swagger_client.models.transaction_summary import TransactionSummary  # noqa: F401,E501


class TransactionDetail(TransactionSummary):
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
        'account_name': 'str',
        'payee_name': 'str',
        'category_name': 'str',
        'subtransactions': 'list[SubTransaction]'
    }
    if hasattr(TransactionSummary, "swagger_types"):
        swagger_types.update(TransactionSummary.swagger_types)

    attribute_map = {
        'account_name': 'account_name',
        'payee_name': 'payee_name',
        'category_name': 'category_name',
        'subtransactions': 'subtransactions'
    }
    if hasattr(TransactionSummary, "attribute_map"):
        attribute_map.update(TransactionSummary.attribute_map)

    def __init__(self, account_name=None, payee_name=None, category_name=None, subtransactions=None, *args, **kwargs):  # noqa: E501
        """TransactionDetail - a model defined in Swagger"""  # noqa: E501
        self._account_name = None
        self._payee_name = None
        self._category_name = None
        self._subtransactions = None
        self.discriminator = None
        self.account_name = account_name
        if payee_name is not None:
            self.payee_name = payee_name
        if category_name is not None:
            self.category_name = category_name
        self.subtransactions = subtransactions
        TransactionSummary.__init__(self, *args, **kwargs)

    @property
    def account_name(self):
        """Gets the account_name of this TransactionDetail.  # noqa: E501


        :return: The account_name of this TransactionDetail.  # noqa: E501
        :rtype: str
        """
        return self._account_name

    @account_name.setter
    def account_name(self, account_name):
        """Sets the account_name of this TransactionDetail.


        :param account_name: The account_name of this TransactionDetail.  # noqa: E501
        :type: str
        """
        if account_name is None:
            raise ValueError("Invalid value for `account_name`, must not be `None`")  # noqa: E501

        self._account_name = account_name

    @property
    def payee_name(self):
        """Gets the payee_name of this TransactionDetail.  # noqa: E501


        :return: The payee_name of this TransactionDetail.  # noqa: E501
        :rtype: str
        """
        return self._payee_name

    @payee_name.setter
    def payee_name(self, payee_name):
        """Sets the payee_name of this TransactionDetail.


        :param payee_name: The payee_name of this TransactionDetail.  # noqa: E501
        :type: str
        """

        self._payee_name = payee_name

    @property
    def category_name(self):
        """Gets the category_name of this TransactionDetail.  # noqa: E501


        :return: The category_name of this TransactionDetail.  # noqa: E501
        :rtype: str
        """
        return self._category_name

    @category_name.setter
    def category_name(self, category_name):
        """Sets the category_name of this TransactionDetail.


        :param category_name: The category_name of this TransactionDetail.  # noqa: E501
        :type: str
        """

        self._category_name = category_name

    @property
    def subtransactions(self):
        """Gets the subtransactions of this TransactionDetail.  # noqa: E501

        If a split transaction, the subtransactions.  # noqa: E501

        :return: The subtransactions of this TransactionDetail.  # noqa: E501
        :rtype: list[SubTransaction]
        """
        return self._subtransactions

    @subtransactions.setter
    def subtransactions(self, subtransactions):
        """Sets the subtransactions of this TransactionDetail.

        If a split transaction, the subtransactions.  # noqa: E501

        :param subtransactions: The subtransactions of this TransactionDetail.  # noqa: E501
        :type: list[SubTransaction]
        """
        if subtransactions is None:
            raise ValueError("Invalid value for `subtransactions`, must not be `None`")  # noqa: E501

        self._subtransactions = subtransactions

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
        if issubclass(TransactionDetail, dict):
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
        if not isinstance(other, TransactionDetail):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
