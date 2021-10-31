from unittest import TestCase


class TestSample(TestCase):
    def test_works(self):
        self.assertTrue(True)

    def test_fails(self):
        self.assertTrue(False)

    def test_raises(self):
        raise Exception("this test raises")
