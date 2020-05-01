"""
Unit test suite for libstax.

To run:
nose2 -v basics
"""

import unittest

from stax.contract import StaxContract


class StaxContractTests(unittest.TestCase):
    """
    Inherited class to run all unit tests for this module
    """

    def setUp(self):
        self.StaxContract = StaxContract

    def testDefaultSchema(self):
        """
        Test the default schema is valid
        """
        schema = self.StaxContract.default_swagger_template()
        self.assertEqual(schema.get("info").get("title"), "Stax Core API")
        self.assertIsInstance(schema.get("components").get("schemas"), dict)

    def testGetSchema(self):
        """
        Test getting the default schema
        """
        data = {"Name": "Unit", "AccountType": "Test"}
        component = "accounts.CreateAccount"
        self.StaxContract.validate(data, component)
        schema = self.StaxContract.get_schema()
        self.assertEqual(schema.get("info").get("title"), "Stax Core API")

    def testSchemaExceptions(self):
        """
        Test the schema exceptions are raised
        """
        data = "unit"
        component = "accounts.ReadAccounts"
        with self.assertRaises(StaxContract.ValidationException):
            self.StaxContract.validate(data, component)

        component = "unit"
        with self.assertRaises(StaxContract.ValidationException):
            self.StaxContract.validate(data, component)


if __name__ == "__main__":
    unittest.main()
