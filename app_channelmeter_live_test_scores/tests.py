# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django_eventstream.storage import DjangoModelStorage, EventDoesNotExist
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


class DjangoStorageTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.storage = DjangoModelStorage()

    def test_empty_channel_id(self):
        self.assertEqual(self.storage.get_current_id('empty'), 0)

    def test_empty_channel_events(self):
        self.assertEqual(self.storage.get_events('empty', 0), [])

    def test_empty_channel_error(self):
        with self.assertRaises(EventDoesNotExist) as cm:
            self.storage.get_events('empty', 1)
        
        self.assertEqual(cm.exception.current_id, 0)

    def test_append(self):
        channel = 'channel'
        data = {'a': 'b'}

        self.storage.append_event(channel, 'message', data)

        self.assertEqual(self.storage.get_current_id(channel), 1)
        
        events = self.storage.get_events(channel, 0)
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].data, data)

        self.assertEqual(self.storage.get_events(channel, 1), [])

        with self.assertRaises(EventDoesNotExist) as cm:
            self.storage.get_events(channel, 2)
        
        self.assertEqual(cm.exception.current_id, 1)

