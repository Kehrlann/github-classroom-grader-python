from unittest import TestCase


class TestA(TestCase):
    def test_works(self):
        self.assertTrue(True)

    def test_fails(self):
        self.assertTrue(False)

    def test_raises(self):
        raise Exception("this test raises")
