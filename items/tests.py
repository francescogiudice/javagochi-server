from django.test import TestCase
from django.test import Client

from rest_framework import status
from rest_framework.authtoken.models import Token

from users.models import CustomUser

from items.models import BaseItem, OwnedItem
from items.scripts import use_item_and_save

class TestItems(TestCase):

    def test_items(self):

        name = 'test'
        email = 'email@test.it'
        pwd = 'TestPwd0'

        c = Client()

        response = c.post('/rest-auth/registration/', {'username': name, 'email': email, 'password1': pwd, 'password2': pwd})
        self.assertTrue(status.is_success(response.status_code))

        response = c.post('/rest-auth/login/', {'username': name, 'password': pwd})
        self.assertTrue(status.is_success(response.status_code))

        user = CustomUser.objects.filter(username=name).first()

        token = Token.objects.filter(user_id=user.id).first()
        key = 'Token ' + token.key
        header = {'HTTP_AUTHORIZATION': key}

        item = 'Simple_food'
        amount = 5

        response = c.post('/api/items/buy/', {'user': name, 'item': item, 'amount': amount}, content_type="application/json", **header)
        self.assertTrue(status.is_success(response.status_code))

        ownedItem = OwnedItem.objects.filter(item__name=item).first()
        self.assertEqual(ownedItem.amount_owned, amount)

        use_item_and_save(ownedItem)
        self.assertEqual(ownedItem.amount_owned, amount-1)
