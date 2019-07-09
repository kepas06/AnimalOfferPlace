from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from offers.models import UserProfile, Offer, Category,Question

from django.utils.translation import gettext_lazy as _


# class SignUpForm(UserCreationForm):
#     first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
#     last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
#     email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

#     class Meta:
#         model = User
#         fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )


class ProfileForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    city = forms.CharField(max_length=100)
    contact = forms.IntegerField()

    class Meta:
        model = User     
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2','city', 'contact')



class OfferForm(ModelForm):
    class Meta:
        model = Offer
        fields = ('title','content','category','price','contact','photo',)
        
    def __init__(self, *args, **kwargs):
        super(OfferForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = "Tytuł"
        self.fields['content'].label = "Treść"
        self.fields['category'].label = "Kategoria"
        self.fields['price'].label = "Cena"
        self.fields['contact'].label = "Kontakt"
        self.fields['photo'].label = "Zdjęcie"
        # widgets = {'slug': forms.HiddenInput, initial=}


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ('title','content','category')
    
    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = "Tytuł"
        self.fields['content'].label = "Treść"
        self.fields['category'].label = "Kategoria"
        

