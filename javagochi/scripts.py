from random import randint

from javagochi.models import Javagochi, JavagochiExpMap
from items.models import OwnedItem, BaseItem
from users.models import CustomUser
from users.scripts import increase_user_level
from items.scripts import use_item_and_save
from consts import *

def check_if_evolves(javagochi):
    if(javagochi.current_level >= javagochi.race.evolves_at):
        javagochi.race = javagochi.race.evolves_into
        javagochi.save()

def increase_javagochi_level(javagochi, amount_to_increase):
    print(("Increasing experience of {} by {} (starting from {})").format(javagochi.nickname, str(amount_to_increase), javagochi.current_experience))
    if(javagochi.current_level >= MAX_JAVAGOCHI_LEVEL):
        print(("{} already reached maximum level. Returning").format(javagochi.nickname))
        return

    needed_exp = JavagochiExpMap.objects.get(level=javagochi.current_level)

    # If there is enough experience to move to the next level, increase the current_level
    # and add the remaining experience. Otherwise just increase the experience
    if(javagochi.current_experience + amount_to_increase >= needed_exp.exp_for_next_level):
        javagochi.current_level += 1
        # Add coins reward to user
        user = javagochi.owner
        user.coins += needed_exp.coins_reward
        user.save()
        # Checks if needs to evolve
        if(javagochi.race.evolves_into):
            check_if_evolves(javagochi)
        # Adds the leftover experience
        new_amount = amount_to_increase - (needed_exp.exp_for_next_level - javagochi.current_experience)
        javagochi.current_experience = 0
        javagochi.save()
        increase_javagochi_level(javagochi, new_amount)
    else:
        javagochi.current_experience += amount_to_increase
    javagochi.save()

def take_damage(javagochi, amount):
    javagochi.current_health -= amount
    if(javagochi.current_health <= 0):
        javagochi.delete()
    else:
        javagochi.save()

def hunger(javagochi, item):
    javagochi.current_hunger = max(javagochi.current_hunger - item.item.amount_modified, 0)
    javagochi.save()
    use_item_and_save(item)

def cold(javagochi, item):
    javagochi.current_cold = max(javagochi.current_hunger - item.item.amount_modified, 0)
    javagochi.save()
    use_item_and_save(item)

def hot(javagochi, item):
    javagochi.current_hot = max(javagochi.current_hunger - item.item.amount_modified, 0)
    javagochi.save()
    use_item_and_save(item)

switcher = {
    "Hunger": hunger,
    "Cold": cold,
    "Hot": hot
}

def use_item(javagochi_id, item_name, username):
    javagochi = Javagochi.objects.filter(id=javagochi_id).first()
    item_type = BaseItem.objects.filter(name=item_name).first()
    user = CustomUser.objects.filter(username=username).first()

    owned_item = OwnedItem.objects.filter(owner=user, item=item_type).first()

    if(owned_item.amount_owned > 0):
        func = switcher.get(item_type.property_modified, "nothing")
        func(javagochi, owned_item)
        increase_user_level(user, item_type.user_exp_on_use)
        increase_javagochi_level(javagochi, item_type.jc_exp_on_use)
        return True
    else:
        return False

def challenge_result(challenger, challenged):

    challenger_str = challenger.race.strength
    challenged_str = challenged.race.strength

    #checking weakness for the challenged javagpchi
    if(challenged.race.type.weakness == challenger.race.type.type):
        challenger_str = challenger_str*2

    #checking weakness for the challenger javagpchi
    if(challenger.race.type.weakness == challenged.race.type.type):
        challenged_str = challenged_str*2

    #"rolling dice" for the javagochi
    challenger_str += randint(1, 50)
    challenged_str += randint(1, 50)

    #checking the highest strength to determine the winning javagochi
    if(challenged_str > challenger_str):
        challenger.owner = challenged.owner
        challenger.save()
        return "Your Javagochi lost the battle. You lost your Javagochi!"
    elif(challenger_str > challenged_str):
        challenged.owner = challenger.owner
        challenged.save()
        return "Your Javagochi won the battle. You aquired your opponent's Javagochi!"
    else:
        return "The battle result was a draw..."
