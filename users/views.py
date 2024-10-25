import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView

from config import settings
from users.forms import UserRegisterForm, UserProfileForm, EmailForm
from users.models import User

class UsersListView(LoginRequiredMixin, ListView):
    model = User

# Create your views here.
class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user_form = form.save(commit=False)
        try:
            send_mail(subject='Подтверждение почты',
                      message='Приветственное сообщение',
                      from_email=settings.EMAIL_HOST_USER,
                      recipient_list=[user_form.email],)
            return super().form_valid(form)
        except:
            return HttpResponseBadRequest("Некорректные данные")

class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

def recover_password(request):
    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = get_object_or_404(User, email=email)
            password = ''.join(random.choices(['1', 'd', 'F', '9', '7', 'R', 'c', '2', 'i', 'O', '0'], k=6))
            user.set_password(password)
            user.save()
            send_mail(subject='Новый пароль',
                      message=f'Новый пароль - {password}',
                      from_email=settings.EMAIL_HOST_USER,
                      recipient_list=[email], )
            return HttpResponseRedirect('/')
    else:
        form = EmailForm()
    return render(request, "users/recover_password.html", {"form": form})


def block_user(request, pk):
    user = User.objects.filter(pk=pk).first()
    user.is_active = True
    user.save()
    return HttpResponseRedirect("/")

def unblock_user(request, pk):
    user = User.objects.filter(pk=pk).first()
    user.is_active = False
    user.save()
    return HttpResponseRedirect("/")
