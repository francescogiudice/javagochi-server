from django.test import TestCase
from django.test import Client

from rest_framework import status
from rest_framework.authtoken.models import Token

from users.models import CustomUser

from javagochi.models import Javagochi, JavagochiBase, JavagochiExpMap

from trades.models import TradeOffer

class TestTrades(TestCase):

    def test_trades(self):

        name = 'test'
        email = 'email@test.it'
        pwd = 'TestPwd0'
        c = Client()

        response = c.post('/rest-auth/registration/', {'username': name, 'email': email, 'password1': pwd, 'password2': pwd})
        self.assertTrue(status.is_success(response.status_code))

        response = c.post('/rest-auth/login/', {'username': name, 'password': pwd})
        self.assertTrue(status.is_success(response.status_code))

        race = 'Charmagochi'
        nick = 'trade'

        user = CustomUser.objects.filter(username=name).first()
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

        offeredId = jc.id
        interestedInto = 'Aligagochi'

        response = c.post('/api/trades/add/', {'offered_id': offeredId, 'interested_into': interestedInto}, content_type="application/json", **header)
        self.assertTrue(status.is_success(response.status_code))

        trade = TradeOffer.objects.filter(offering=jc.id).first()
        interestedRace = trade.interested_into.race
        self.assertEqual(interestedRace, interestedInto)
