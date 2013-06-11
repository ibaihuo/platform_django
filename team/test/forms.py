#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django.contrib.auth.models import User
from django.test import TestCase

from team import forms

class SubmitFormTests(TestCase):
    """
    Test the submit form
    """
    def test_registration_form(self):
        """
        Test that ``RegistrationForm`` enforces username constraints
        and matching passwords.
        """
        invalid_data_dicts = [
            # Non-alphanumeric username.
            {'data': {'username': 'foo/bar',
                      'email': 'foo@example.com',
                      'password1': 'foo',
                      'password2': 'foo'},
            'error': ('username', [u"This value must contain only letters, numbers and underscores."])},
            # Already-existing username.
            {'data': {'username': 'alice',
                      'email': 'alice@example.com',
                      'password1': 'secret',
                      'password2': 'secret'},
            'error': ('username', [u"A user with that username already exists."])},
            # Mismatched passwords.
            {'data': {'username': 'foo',
                      'email': 'foo@example.com',
                      'password1': 'foo',
                      'password2': 'bar'},
            'error': ('__all__', [u"The two password fields didn't match."])},
            ]

        for invalid_dict in invalid_data_dicts:
            form = forms.SubmitForm(data=invalid_dict['data'])
            self.failIf(form.is_valid())
            self.assertEqual(form.errors[invalid_dict['error'][0]],
                             invalid_dict['error'][1])

        self.failUnless(form.is_valid())
