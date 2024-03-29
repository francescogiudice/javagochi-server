from django.test import TestCase
from django.test import Client

from rest_framework import status
from rest_framework.authtoken.models import Token

from users.models import CustomUser, ExpMap
from users.scripts import increase_user_level

class TestUsers(TestCase):

    def test_users(self):

        name = 'test'
        wrong_name = 'aaaa'
        email = 'email@test.it'
        pwd = 'TestPwd0'
        wrong_pwd = 'pwd'
        c = Client()

        response = c.post('/rest-auth/registration/', {'username': name, 'email': email, 'password1': pwd, 'password2': pwd})
        self.assertTrue(status.is_success(response.status_code))

        user = CustomUser.objects.filter(username=name).first()
        self.assertEqual(user.coins, 1000)
        self.assertEqual(user.level, 1)
        self.assertEqual(user.exp, 0)

        response = c.post('/rest-auth/login/', {'username': name, 'password': pwd})
        self.assertTrue(status.is_success(response.status_code))

        response = c.post('/rest-auth/login/', {'username': wrong_name, 'password': pwd})
        self.assertTrue(status.is_client_error(response.status_code))

        response = c.post('/rest-auth/login/', {'username': name, 'password': wrong_pwd})
        self.assertTrue(status.is_client_error(response.status_code))

        token = Token.objects.filter(user_id=user.id).first()
        self.assertIsNotNone(token)

        needed_exp = ExpMap.objects.get(level=user.level)
        old_level = user.level
        new_exp = needed_exp.exp_for_next_level - 1
        old_exp = user.exp

        increase_user_level(user, new_exp)
        self.assertEqual(user.exp, old_exp + new_exp)

        increase_user_level(user, 1)
        self.assertEqual(user.level, old_level + 1)

        response = c.post('/rest-auth/logout/')
        self.assertTrue(status.is_success(response.status_code))
