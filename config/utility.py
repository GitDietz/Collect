from hashlib import sha1 as sha_constructor
import logging
import re
import uuid
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

# ############## General functions #####################
def create_next_increment_name(name):
    pattern = r"(^[a-zA-Z '-]+)([0-9]+)"
    match = re.match(pattern, name)
    if match:
        increment = match.group(2)
        new_inc = int(increment) + 1
        new_name = match.group(1) + str(new_inc)
        name_length = len(match.group(1))

        if len(new_name) > 30:
            new_name = match.group(1)[:name_length-1] + str(new_inc)
        return new_name
    else:
        return name + '1'


def create_key():
    salt = uuid.uuid4().hex
    key = sha_constructor(salt.encode()).hexdigest()
    logging.getLogger("info_logger").info(f'created key is {key}')
    return key


def is_existing_user(email):
    if User.objects.filter(email=email).exists():
        return True
    else:
        return False


def create_username(first_name, last_name):
    logging.getLogger("info_logger").info(f'no username yet')

    new_username = first_name[:15] + last_name[:10]
    new_username.replace(' ', '')
    this_user = User.objects.all().filter(Q(username__iexact=new_username))

    while this_user.exists():
        new_username = create_next_increment_name(new_username)
        this_user = User.objects.all().filter(Q(username__iexact=new_username))
    return new_username
