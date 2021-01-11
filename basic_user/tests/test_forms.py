from basic_user.forms import SignUpForm
from django.test import TransactionTestCase


class TestForms(TransactionTestCase):
    def test_signup_form_valid_data(self):
        form = SignUpForm(data={
            'username': 'testusername',
            'full_name': 'test_full_name',
            'email': 'email@test.com',
            'password': 'testing321',
            'password1': 'testing321',
            'password2': 'testing321'
        })
        print(form.errors)
        self.assertTrue(form.is_valid())
        
    def test_signup_form_no_data(self):
        form = SignUpForm(data={})
        self.assertFalse(form.is_valid())
        print(form.errors)
        self.assertEqual(len(form.errors), 5)
        
