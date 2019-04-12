def use_item_and_save(item):
    item.amount_owned -= 1
    if(item.amount_owned <= 0):
        item.delete()
    else:
        item.save()
