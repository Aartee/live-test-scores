from django.test import TestCase
from rest_framework.test import RequestsClient

# Create your tests here.

class LiveTestScoresTestCase(TestCase):

    def setUp(self):
        self.client = RequestsClient()

    def test_if_students_endpoint_running(self):
        """
        Checking if students endpoint is up and running
        """
        response = self.client.get('http://localhost:8000/students/')
        assert response.status_code == 200

    def test_if_exams_endpoint_running(self):
        """
        Checking if exams endpoint is up and running
        """
        response = self.client.get('http://localhost:8000/exams/')
        assert response.status_code == 200
