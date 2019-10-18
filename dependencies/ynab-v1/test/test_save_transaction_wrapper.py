# coding: utf-8

"""
    YNAB API Endpoints

    Our API uses a REST based design, leverages the JSON data format, and relies upon HTTPS for transport. We respond with meaningful HTTP response codes and if an error occurs, we include error details in the response body.  API Documentation is at https://api.youneedabudget.com  # noqa: E501

    OpenAPI spec version: 1.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

import swagger_client
from models.save_transaction_wrapper import SaveTransactionWrapper  # noqa: E501
from swagger_client.rest import ApiException


class TestSaveTransactionWrapper(unittest.TestCase):
    """SaveTransactionWrapper unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testSaveTransactionWrapper(self):
        """Test SaveTransactionWrapper"""
        # FIXME: construct object with mandatory attributes with example values
        # model = swagger_client.models.save_transaction_wrapper.SaveTransactionWrapper()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()