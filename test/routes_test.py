import unittest
from app import routes


class MyTestCase(unittest.TestCase):
    def testhasActiveAccount(self):
        result = routes.ping()
        expected = "<p>Ping!</p>"
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
