from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Product#, Person
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from django.utils.translation import ugettext_lazy as _


from django.utils.safestring import mark_safe
class CustomUserCreationForm(UserCreationForm, forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Repeat password')

    class Meta:
        model=CustomUser
        fields=('username',
                'first_name', 
                'last_name', 
                'address', 
                'country', 
                'email',
                'password1',
                'password2') 
        widgets = {'country': CountrySelectWidget()}
        
        
    def save(self, commit=True):
        user=super(CustomUserCreationForm, self).save(commit=False)
        user.first_name=self.cleaned_data['first_name']
        user.last_name=self.cleaned_data['last_name']
        user.email=self.cleaned_data['email']
        
        if commit:
            user.save()
        
        return user 

class CustomUserChangeForm(UserChangeForm, forms.ModelForm):
    
    class Meta:
        model=CustomUser
        fields=('username',
                'first_name', 
                'last_name', 
                'address', 
                'country', 
                'email',
                'password') 
        widgets = {'country': CountrySelectWidget()}
 
        
class ProductCreationForm(forms.ModelForm):
    
    class Meta:
        model=Product
        fields=('price', 
                'title', 
                'descr', 
                'product_image', 
                'country', 
                'category')
        labels = {
            "title": _("Name"),
            "descr": _("Description"),
        } 
        
        widgets = {'country': CountrySelectWidget()}
        
        