import logging
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import ( authenticate, get_user_model, login, logout )
from django.db.models import Q

#from .models import InvitationKey
from the_list.models import ShopGroup


class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField(label='Email Address', required=True)  # overrides the default
    email2 = forms.EmailField(label='Confirm Email')
    first_name = forms.CharField(label='First Name (will display for others)', required=True)
    last_name = forms.CharField(label='Last Name', required=True)
    password = forms.CharField(widget=forms.PasswordInput)
    joining = forms.CharField(label='Group to create', max_length=100)
    purpose = forms.CharField(label='What is this group for?', max_length=200)

    class Meta:
        model = User
        fields = ['email', 'email2',
            'first_name', 'last_name',
            'password', 'joining', 'purpose']

    def clean_email2(self):  # this is 2 so it runs off the email2 field
        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email2')
        print(f'first is {email}, second is {email2}')
        if email != email2:
            raise ValidationError('Emails are not the same')

        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise ValidationError('Emails already exists for a user, please enter another one')
        return email2


    def clean_joining(self):
        target_group = self.cleaned_data.get('joining')
        # now check that the group does not exists and create it, rather do this in the form
        qs_shop_group = ShopGroup.objects.all()
        this_found = qs_shop_group.filter(Q(name__iexact=target_group))
        if this_found.exists():
            raise ValidationError('That group already exists, please enter another name')

        return target_group
