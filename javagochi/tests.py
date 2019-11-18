from django.test import TestCase
from django.test import Client

from rest_framework import status
from rest_framework.authtoken.models import Token

from users.models import CustomUser

from items.models import BaseItem, OwnedItem
from items.scripts import use_item_and_save

from javagochi.models import Javagochi, JavagochiBase, JavagochiExpMap
from javagochi.scripts import check_if_evolves, take_damage

class TestJavagochi(TestCase):

    def test_javagochi(self):

        name = 'test'
        email = 'email@test.it'
        pwd = 'TestPwd0'

        c = Client()

        response = c.post('/rest-auth/registration/', {'username': name, 'email': email, 'password1': pwd, 'password2': pwd})
        self.assertTrue(status.is_success(response.status_code))

        response = c.post('/rest-auth/login/', {'username': name, 'password': pwd})
        self.assertTrue(status.is_success(response.status_code))

        user = CustomUser.objects.filter(username=name).first()
        user.coins = 1000000
        user.save()

        # test buy javagochi
        race = 'Bulbagochi'
        nick = 'test'

        jc_race = JavagochiBase.objects.filter(race=race).first()

        self.assertTrue(user.level >= jc_race.min_user_level)
        self.assertTrue(user.coins >= jc_race.cost)

        token = Token.objects.filter(user_id=user.id).first()
        key = 'Token ' + token.key
        header = {'HTTP_AUTHORIZATION': key}

        response = c.post('/api/javagochi/buy/', {'user': name, 'race': race, 'nickname': nick}, content_type="application/json", **header)
        self.assertTrue(status.is_success(response.status_code))

        jc = Javagochi.objects.filter(nickname=nick).first()
        self.assertEqual(jc.race.race, race)

        # test javagochi evolution
        evolves_into = jc.race.evolves_into.race
        jc.current_level = jc.race.evolves_at
        check_if_evolves(jc)

        self.assertEqual(jc.race.race, evolves_into)

        # test javagochi health system
        self.assertEqual(jc.current_health, jc.race.max_health)

        damage = 10
        take_damage(jc, damage)
        self.assertEqual(jc.current_health, jc.race.max_health-damage)

        # test use items
        item = 'Simple_food'
        amount = 5
        current = 50

        jc.current_hunger = current
        jc.current_hot = current
        jc.current_cold = current

        jc.save()

        response = c.post('/api/items/buy/', {'user': name, 'item': item, 'amount': str(amount)}, content_type="application/json", **header)
        self.assertTrue(status.is_success(response.status_code))

        ownedItem = OwnedItem.objects.filter(item__name=item).first()
        self.assertEqual(ownedItem.amount_owned, amount)
        self.assertTrue(ownedItem.owner.username, name)

        id = str(jc.id)

        response = c.put('/api/javagochi/owned/' + id + '/useitem/', {'item': ownedItem.item.name, 'user': ownedItem.owner.username}, content_type="application/json", **header)
        self.assertTrue(status.is_success(response.status_code))

        jc = Javagochi.objects.filter(nickname=nick).first()
        ownedItem = OwnedItem.objects.filter(item__name=item).first()

        self.assertEqual(ownedItem.amount_owned, amount-1)
        self.assertEqual(jc.current_hunger, current - ownedItem.item.amount_modified)
        #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        jc.current_hunger = current
        jc.current_hot = current
        jc.current_cold = current

        jc.save()

        item = 'Cold_water'
        amount = 5

        response = c.post('/api/items/buy/', {'user': name, 'item': item, 'amount': str(amount)}, content_type="application/json", **header)
        self.assertTrue(status.is_success(response.status_code))

        ownedItem = OwnedItem.objects.filter(item__name=item).first()
        self.assertEqual(ownedItem.amount_owned, amount)
        self.assertTrue(ownedItem.owner, name)

        response = c.put('/api/javagochi/owned/' + id + '/useitem/', {'item': ownedItem.item.name, 'user': ownedItem.owner.username}, content_type="application/json", **header)
        self.assertTrue(status.is_success(response.status_code))

        jc = Javagochi.objects.filter(nickname=nick).first()
        ownedItem = OwnedItem.objects.filter(item__name=item).first()

        self.assertEqual(ownedItem.amount_owned, amount-1)
        self.assertEqual(jc.current_hot, current - ownedItem.item.amount_modified)
        #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        jc.current_hunger = current
        jc.current_hot = current
        jc.current_cold = current

        jc.save()

        item = 'Steak'
        amount = 5

        response = c.post('/api/items/buy/', {'user': name, 'item': item, 'amount': str(amount)}, content_type="application/json", **header)
        self.assertTrue(status.is_success(response.status_code))

        ownedItem = OwnedItem.objects.filter(item__name=item).first()
        self.assertEqual(ownedItem.amount_owned, amount)
        self.assertTrue(ownedItem.owner, name)

        response = c.put('/api/javagochi/owned/' + id + '/useitem/', {'item': ownedItem.item.name, 'user': ownedItem.owner.username}, content_type="application/json", **header)
        self.assertTrue(status.is_success(response.status_code))

        jc = Javagochi.objects.filter(nickname=nick).first()
        ownedItem = OwnedItem.objects.filter(item__name=item).first()

        self.assertEqual(ownedItem.amount_owned, amount-1)
        self.assertEqual(jc.current_hunger, current - ownedItem.item.amount_modified)
        #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        jc.current_hunger = current
        jc.current_hot = current
        jc.current_cold = current

        jc.save()

        item = 'Hot_drink'
        amount = 5

        response = c.post('/api/items/buy/', {'user': name, 'item': item, 'amount': str(amount)}, content_type="application/json", **header)
        self.assertTrue(status.is_success(response.status_code))

        ownedItem = OwnedItem.objects.filter(item__name=item).first()
        self.assertEqual(ownedItem.amount_owned, amount)
        self.assertTrue(ownedItem.owner, name)

        response = c.put('/api/javagochi/owned/' + id + '/useitem/', {'item': ownedItem.item.name, 'user': ownedItem.owner.username}, content_type="application/json", **header)
        self.assertTrue(status.is_success(response.status_code))

        jc = Javagochi.objects.filter(nickname=nick).first()
        ownedItem = OwnedItem.objects.filter(item__name=item).first()

        self.assertEqual(ownedItem.amount_owned, amount-1)
        self.assertEqual(jc.current_cold, current - ownedItem.item.amount_modified)
        #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        # kill the test javagochi
        take_damage(jc, jc.current_health)

        jc = Javagochi.objects.filter(nickname=nick).first()
        self.assertIsNone(jc)

        # test battle
        user.level = 45
        user.coins = 1000000

        user.save()

        race = 'Alphagochi'
        nick = 'Alpha'

        response = c.post('/api/javagochi/buy/', {'user': name, 'race': race, 'nickname': nick}, content_type="application/json", **header)
        self.assertTrue(status.is_success(response.status_code))

        jc = Javagochi.objects.filter(nickname=nick).first()
        id_challenged = jc.id

        name2 = 'test2'
        email = 'email@test2.it'
        pwd = 'TestPwd0'

        c = Client()

        response = c.post('/rest-auth/registration/', {'username': name2, 'email': email, 'password1': pwd, 'password2': pwd})
        self.assertTrue(status.is_success(response.status_code))

        response = c.post('/rest-auth/login/', {'username': name2, 'password': pwd})
        self.assertTrue(status.is_success(response.status_code))

        race = 'Bulbagochi'
        nick = 'Bulba'

        response = c.post('/api/javagochi/buy/', {'user': name2, 'race': race, 'nickname': nick}, content_type="application/json", **header)
        self.assertTrue(status.is_success(response.status_code))

        jc = Javagochi.objects.filter(nickname=nick).first()
        id_challenger = jc.id

        response = c.put('/api/javagochi/' + str(id_challenged) + '/challenge/', {'id_challenger': str(id_challenger)}, content_type="application/json", **header)
        self.assertTrue(status.is_success(response.status_code))

        jc = Javagochi.objects.filter(nickname=nick).first()
        self.assertTrue(jc.owner.username, name)

        # test that a user can't buy javagochi with requirements the users doesn't meet
        user.coins = 1
        user.level = 1
        user.save()

        race = 'Alphagochi'
        nick = 'false_test'

        jc_race = JavagochiBase.objects.filter(race=race).first()

        self.assertFalse(user.level >= jc_race.min_user_level)
        self.assertFalse(user.coins >= jc_race.cost)

        response = c.post('/api/javagochi/buy/', {'user': name, 'race': race, 'nickname': nick}, content_type="application/json", **header)

        # assert doesn't exist
        jc = Javagochi.objects.filter(nickname=nick).first()
        self.assertIsNone(jc)
