import unittest
import app


class MyTestCase(unittest.TestCase):
    def testhasActiveAccount(self):
        result = app.hasActiveAccount("not an id")
        self.assertEqual(result, False)


if __name__ == '__main__':
    unittest.main()