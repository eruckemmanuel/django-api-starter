from django.test import TestCase
from django.test import Client


class TestUserAPI(TestCase):
    def setUpTestData(cls):
        pass

    def setUp(self):
        self.client = Client()
