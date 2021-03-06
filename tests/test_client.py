"""
Unit test suite for libstax.

To run:
nose2 -v basics
"""

import responses
import unittest

from staxapp.api import Api
from staxapp.config import Config
from staxapp.openapi import StaxClient
from staxapp.exceptions import ApiException, ValidationException


class StaxClientTests(unittest.TestCase):
    """
    Inherited class to run all unit tests for this module
    """

    def setUp(self):
        self.Api = Api
        self.Api._requests_auth = lambda x, y: (x, y)

        self.account_client = StaxClient("accounts")
        self.workload_client = StaxClient("workloads")
        self.assertTrue(self.account_client._initialized)
        self.assertTrue(self.workload_client._initialized)

    def testStaxClient(self):
        """
        Test initializing Stax client
        """
        client = StaxClient("accounts", lambda_client=True)
        self.assertTrue(client._initialized)
        self.assertTrue(client._admin)

    def testInvalidStaxClient(self):
        """
        Test an invalid Api class raises an error
        """
        with self.assertRaises(ValidationException):
            StaxClient("fake")

    def testLoadOldSchema(self):
        """
        Test loading Old schema
        """
        self.Config = Config
        self.Config.load_live_schema = False
        client = StaxClient("accounts", force=True)
        self.assertTrue(client._initialized)

    @responses.activate
    def testStaxWrapper(self):
        """
        Test the Stax client wrapper
        """
        # Test a valid GET
        response_dict = {"Status": "OK"}
        responses.add(
            responses.GET,
            f"{Config.api_base_url()}/accounts",
            json=response_dict,
            status=200,
        )
        response = self.account_client.ReadAccounts()
        self.assertEqual(response, response_dict)

        # Test a valid GET with path params
        response_dict = {"Status": "OK"}
        responses.add(
            responses.GET,
            f"{Config.api_base_url()}/accounts/fake-id",
            json=response_dict,
            status=200,
        )
        params = {"account_id": "fake-id", "Unit": "Test"}
        response = self.account_client.ReadAccounts(**params)
        self.assertEqual(response, response_dict)

        # Test a valid GET with params
        response_dict = {"Status": "OK"}
        responses.add(
            responses.GET,
            f"{Config.api_base_url()}/accounts",
            json=response_dict,
            status=200,
        )
        params = {"Unit": "Test"}
        response = self.account_client.ReadAccounts(**params)
        self.assertEqual(response, response_dict)

        # Test a valid POST
        response_dict = {"Status": "OK"}
        responses.add(
            responses.POST,
            f"{Config.api_base_url()}/accounts",
            json=response_dict,
            status=200,
        )
        response = self.account_client.CreateAccount(Name="Unit", AccountType="ab13a455-033f-4947-8393-641eefc3ba5e")
        self.assertEqual(response, response_dict)

    @responses.activate
    def testStaxWrapperErrors(self):
        """
        Test raising errors in StaxWrapper
        """
        # To ensure it fails on the assertion not calling the response
        response_dict = {"Error": "A unique UnitTest error for workload catalogues"}

        responses.add(
            responses.GET,
            f"{Config.api_base_url()}/workload-catalogue/fake-id/fake-id",
            json=response_dict,
            status=400,
        )
        # Test an error occurs when the wrong client is used
        with self.assertRaises(ValidationException):
            self.account_client.ReadCatalogueVersion(
                catalogue_id="fake-id", version_id="fake-id"
            )
        # Test an error occurs when a parameter is missing
        with self.assertRaises(ValidationException):
            self.workload_client.ReadCatalogueVersion(version_id="fake-id/fake-id")
        # Test an error occurs when error in response
        with self.assertRaises(ApiException):
            self.workload_client.ReadCatalogueVersion(
                catalogue_id="fake-id", version_id="fake-id"
            )


if __name__ == "__main__":
    unittest.main()
