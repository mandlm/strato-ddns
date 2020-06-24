import unittest
from .ddns_update import response_successful

class TestDdnsUpdate(unittest.TestCase):

    def test_response_successful(self):
        self.assertTrue(response_successful("good"))
        self.assertTrue(response_successful("good 1.2.3.4"))
        self.assertTrue(response_successful("good abcd:abcd:abcd:abcd:abcd:abcd:abcd:abcd"))
        self.assertTrue(response_successful("nochg"))
        self.assertTrue(response_successful("nochg 1.2.3.4"))
        self.assertTrue(response_successful("nochg abcd:abcd:abcd:abcd:abcd:abcd:abcd:abcd"))
        self.assertFalse(response_successful("notfqdn"))
        self.assertFalse(response_successful("nohost"))
        self.assertFalse(response_successful("numhost"))
        self.assertFalse(response_successful("abuse"))
        self.assertFalse(response_successful("badagent"))
        self.assertFalse(response_successful("dnserr"))
        self.assertFalse(response_successful("911"))

