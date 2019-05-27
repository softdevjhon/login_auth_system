from django.shortcuts import render
from django.views.generic.edit import FormView
from django.contrib.auth import login
from core.forms import RegisterForm, LoginForm
from django.contrib.auth.models import User


class RegisterFormView(FormView):
    form_class = RegisterForm
    success_url = "/login/"
    template_name = "register.html"
    
    
    def form_valid(self, form):
        """ Save user if registration form valid """
        form.save()
        return super(RegisterFormView, self).form_valid(form)



class LoginFormView(FormView):
    form_class = LoginForm
    template_name = "login.html"
    success_url = "/dashboard"


    def form_valid(self, form):
        """ Login user if login form valid """
        self.user = form.get_user()
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)