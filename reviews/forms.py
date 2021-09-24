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
    headline = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}))
    rating = forms.IntegerField(widget=forms.NumberInput(attrs={'size': '3', 'min': '1','max': '5'}))
    body = forms.CharField(widget=forms.Textarea(attrs={'cols': '75', 'rows': '10'}))
    class Meta:
        model = Review
        fields = ('headline', 'rating', 'body')
