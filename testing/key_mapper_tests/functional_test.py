import unittest
from src.secapi_tl.key_mapper import get_cik, is_registered


class TestCase(unittest.TestCase):

    def test_functional_get_cik(self):
        cik = get_cik("AAPL")
        self.assertEqual(cik, "320193")
        cik = get_cik("msft")
        self.assertEqual(cik, "789019")


    def test_functional_is_registered(self):
        self.assertTrue(is_registered("cost"))
        self.assertFalse(is_registered("iasbesf"))
