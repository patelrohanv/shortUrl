import unittest
import api


class MyTestCase(unittest.TestCase):
    def testhasActiveAccount(self):
        result = api.ping()
        expected = "<p>Ping!</p>"
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
