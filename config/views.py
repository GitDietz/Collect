import datetime
from hashlib import sha1 as sha_constructor
import logging
import re
from urllib.parse import urlencode
import uuid

from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect, Http404, HttpResponse
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .emailer import email_confirmation, email_main, email_reset
from .forms import UserRegisterForm  #, UserLoginForm, UserLoginEmailForm, InvitationKeyForm, InvitationAcceptForm, ResetForm
# from lcore.utils import in_post
# from .models import InvitationKey
from .token import account_activation_token
from .utility import create_username

User = get_user_model()


# def register_view(request):
#     """
#     register as a complete unknown and uninvited visitor
#     settings can disable the view
#     """
#     logging.getLogger("info_logger").info(f'Enter')
#     next = request.GET.get('next')
#     if request.user.is_authenticated:
#         return redirect('/')
#
#     if 'REGISTRATIONS' in dir(settings) and settings.ACCOUNT_ALLOW_REGISTRATION:
#         logging.getLogger("info_logger").info(f'Registration allowed')
#         title = 'Register'
#         form = UserRegisterForm(request.POST or None)
#         if form.is_valid():
#             target_group = form.cleaned_data.get('joining')
#             # to be valid it was checked to not exist
#
#             user = form.save(commit=False)
#             user.is_active = False
#             user.username = create_username(user.first_name, user.last_name)
#             password = form.cleaned_data.get('password')
#             user.set_password(password)
#             user.backend = 'django.contrib.auth.backends.ModelBackend'
#             user.save()
#             logging.getLogger("info_logger").info(f'Saved user')
#
#             new_group = ShopGroup.objects.create_group(target_group, user)
#             new_group.purpose = form.cleaned_data.get('purpose')
#             new_group.save()
#
#             coded_user = force_text(urlsafe_base64_encode(force_bytes(user.pk)))
#             coded_group = force_text(urlsafe_base64_encode(force_bytes(new_group.id)))
#             token = account_activation_token.make_token(user)
#
#             email_kwargs = {"user": user.first_name,
#                             "coded_user": coded_user,
#                             'coded_group': coded_group,
#                             "token": token,
#                             "group_name": target_group,
#                             "destination": user.email,
#                             "subject": "Confirm your registration"}
#             send_result = email_confirmation(user.pk, **email_kwargs)
#             return redirect('account_activation_sent')
#
#         else:
#             context = {'form': form,
#                        'title': title}
#             return render(request, "login_form.html", context)
#     else:
#         logging.getLogger("info_logger").info(f'Registration disabled')
#         return render(request, "temp_register.html", {})
