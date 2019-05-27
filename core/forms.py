from random import choice
from string import ascii_letters
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    """ Custom form for registration """
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label='First Name', min_length=3, max_length=20)
    last_name = forms.CharField(label='Last Name', max_length=20)
    
    
    def __init__(self, *args, **kwargs):
        """
        Deleting useless fields from form and require to enter first name, last name and email in form
        
        """
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields.pop('username')
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True


    def save(self):
        """
        Saving user and assign random username as it's required field in User model
        """
        self.instance.email = self.cleaned_data["email"]
        self.instance.first_name = self.cleaned_data['first_name']
        self.instance.last_name = self.cleaned_data['last_name']
        random = ''.join([choice(ascii_letters) for i in range(30)])
        self.instance.username = random
        return super(RegisterForm, self).save()
 
    
    def clean(self):
        """
        Raise ValidationError if somebody try to register on email, that already registered
        
        """
        try:
            User.objects.get(email=self.cleaned_data['email'])
        except User.DoesNotExist:
            return super(RegisterForm, self).clean()
        except KeyError:
            raise forms.ValidationError('Incorrect email')
        raise forms.ValidationError('Person with that email already exists!')

        
class LoginForm(AuthenticationForm):
    """ Custom form for authentication """
    email = forms.EmailField(label = 'email')
    
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields.pop('username')
        
        
    def clean(self):
        """
        Raising ValidationError if user doesn't exist and if user exists find his username in database
        
        """
        try:
            user = User.objects.get(email=self.cleaned_data['email'])
        except User.DoesNotExist:
            flag = True
            raise forms.ValidationError('Incorrect email or password')
        except KeyError:
            pass
        else:
            self.cleaned_data['username'] = user.username
        return super(LoginForm, self).clean()