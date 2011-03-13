"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client
from django.contrib import auth
from django.contrib.auth.models import User
from shade.social.models import Message
import datetime

class MessagingTest(TestCase):
    def setUp(self):
        now = datetime.datetime.now()
        self.client = Client()
        self.user = User.objects.create_user('test', 'test@test.com',
                'testpassword')
        self.client.login(username='test', password='testpassword')
        self.message = Message(author=self.user, recipient=self.user,
                subject="Test", body="Test", read=False, sent=now)

    def test_inbox(self):
        response = self.client.get('/inbox/')
        self.failUnlessEqual(response.status_code, 200)

    def msg_view_test(self):
        response = self.client.get('/inbox/view/'+self.message.id)
        self.failUnlessEqual(response.status_code, 200)

    def msg_compose_test(self):
        response = self.client.get('/inbox/compose/')
        self.failUnlessEqual(response.status_code, 200)

    def msg_delete_test(self):
        response = self.client.get('/inbox/delete'+self.message.id)
        self.failUnlessEqual(response.status_code, 200)

class AuthTest(TestCase):
    def login_test(self):
        response = self.client.get('/login/')
        self.failUnlessEqual(response.status_code, 200)

    def logout_test(self):
        response = self.client.get('/logout/')
        self.failUnlessEqual(response.status_code, 200)

    def register_test(self):
        response = self.client.get('/register/')
        self.failUnlessEqual(response.status_code, 200)

