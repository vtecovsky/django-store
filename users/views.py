from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, TemplateView
from django.contrib.auth.views import LoginView
from django.shortcuts import HttpResponseRedirect

from django.contrib.messages.views import SuccessMessageMixin
from common.views import TitleMixin

from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from products.models import Basket
from users.models import User, EmailVerification


class UserRegistrationView(SuccessMessageMixin, TitleMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = "users/registration.html"
    success_url = reverse_lazy("users:login")
    success_message = "Вы успешно зарегистрированы"

    title = "Store - Регистрация"

    def get_context_data(self, **kwargs):
        context = super(UserRegistrationView, self).get_context_data()
        return context


class UserLoginView(TitleMixin, LoginView):
    template_name = "users/login.html"
    form_class = UserLoginForm

    title = "Store - Авторизация"


class UserProfileView(TitleMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = "users/profile.html"

    title = "Store - Личный кабинет"

    def get_success_url(self):
        """Передает дополнительные параметры в url путь"""
        return reverse_lazy("users:profile", args=(self.object.id,))

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data()
        context["baskets"] = Basket.objects.filter(user=self.object)
        return context


class EmailVerificationView(TitleMixin, TemplateView):
    title = 'Store - Подтверждение электронной почты'
    template_name = 'users/email_verification.html'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verifications = EmailVerification.objects.filter(user=user, code=code)
        if email_verifications.exists() and not email_verifications.first().is_expired():
            user.is_verified_email = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('index'))
