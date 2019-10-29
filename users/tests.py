from django.test import TestCase
from users.models import CustomUser
from users.scripts import increase_user_level
from django.test import Client

class TestScripts(TestCase):

    def test_users_script(self):
        test_exp = 50
        user = CustomUser.objects.filter(username='fra').first()
        old_exp = user.exp
        increase_user_level(user, test_exp)
        self.assertEqual(user.exp, old_exp + test_exp)

    def test_user_login(self):
        c = Client()
        response = c.post('/rest-auth/login/', {'username': 'fra', 'password': 'fra'})
        self.assertEqual(response.status_code, 200)
