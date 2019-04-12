from users.models import CustomUser, ExpMap
from consts import *

def increase_user_level(user, amount_to_increase):
    print(("Increasing experience of {} by {} (starting from {})").format(user.username, str(amount_to_increase), user.exp))
    if(user.level >= MAX_USER_LEVEL):
        print(("{} already reached maximum level. Returning").format(user.username))
        return

    needed_exp = ExpMap.objects.get(level=user.level)

    if(user.exp + amount_to_increase >= needed_exp.exp_for_next_level):
        user.level += 1
        user.coins += needed_exp.coins_reward
        new_amount = amount_to_increase - (needed_exp.exp_for_next_level - user.exp)
        user.exp = 0
        user.save()
        increase_user_level(user, new_amount)
    else:
        user.exp += amount_to_increase
    user.save()
