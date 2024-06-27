import secrets

from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetView
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView

from config.settings import EMAIL_HOST_USER
from users.forms import UserRegisterForm
from users.models import User


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(20)
        user.token = token
        user.save(update_fields=['token', 'is_active'])
        host = self.request.get_host()
        url = f'https://{host}/users/email_confirm/{token}/'
        send_mail(
            subject='Подтверждение почты',
            message=f'Подтвердите вашу регистрацию перейдя по ссылке {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return super().form_valid(form)


def email_confirm(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


class GeneratePasswordView(PasswordResetView):
    form_class = PasswordResetForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)
            if user:
                password = User.objects.make_random_password(length=8)
                user.set_password(password)
                user.save(update_fields=['password'])
                send_mail(
                    'Смена пароля',
                    f'Ваш новый пароль: {password}',
                    from_email=EMAIL_HOST_USER,
                    recipient_list=[user.email],
                )
            return redirect(reverse("users:login"))
