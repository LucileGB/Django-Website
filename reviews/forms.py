from django import forms

from .models import Review, Ticket

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class NewTicket(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('title', 'description', 'image')


class AnswerTicket(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('headline', 'rating', 'body')
