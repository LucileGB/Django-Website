from django import forms

from .models import Review, Ticket

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class TicketForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'size': '78'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'cols': '75', 'rows': '10'}))

    class Meta:
        model = Ticket
        fields = ('title', 'description', 'image')


class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        ]
    headline = forms.CharField(widget=forms.TextInput(attrs={'size': '78'}))
    rating = forms.CharField(widget=forms.RadioSelect(choices=RATING_CHOICES))
    body = forms.CharField(widget=forms.Textarea(attrs={'cols': '75', 'rows': '10'}))

    class Meta:
        model = Review
        fields = ('headline', 'rating', 'body')
