
from dataclasses import fields
from django.core.exceptions import ValidationError
import datetime
from django import forms
from django.forms import ModelForm
from .models import TrainerProfile, Pokemon, PokemonInstance, Move, Type, Gender
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class PokemonInstanceForm(ModelForm):
    class Meta:
        model = PokemonInstance
        fields = ('nickname','level','date_of_birth','trainer','gender','moves')

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', )
