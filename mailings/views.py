from tempfile import template

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.defaulttags import comment
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DeleteView, DetailView, CreateView, UpdateView, TemplateView

from blog.models import Post
from mailings.forms import NotificationForm
from mailings.models import Notification, Message, Client, NotificationAttempt
from blog.services import get_cached_posts
from mailings.services import get_cached_mailing_count, get_cached_active_mailings, get_cached_users_count


# Create your views here.
class IndexView(TemplateView):
    template_name = 'mailings/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mailing_count'] = get_cached_mailing_count()
        context['active_mailings'] = get_cached_active_mailings()
        context['users_count'] = get_cached_users_count()
        context['posts'] = get_cached_posts()[:3]
        return context




class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(creator=self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data()
        context_data['period'] = {'w': 'Раз в неделю', 'd': 'Раз в день', 'm': 'Раз в месяц'}
        context_data['status'] = {'f':'Завершена', 'c': 'Создана', 'p': 'Запущена'}
        return context_data

class NotificationDetailView(DetailView):
    model = Notification


class NotificationCreateView(LoginRequiredMixin, CreateView):
    model = Notification
    form_class = NotificationForm
    success_url = reverse_lazy('mailings:notifications')

    def form_valid(self, form):
        fields = form.save(commit=False)
        fields.creator = self.request.user
        fields.save()
        return super().form_valid(form)

class NotificationUpdateView(LoginRequiredMixin, UpdateView):
    model = Notification
    form_class = NotificationForm

    def get_success_url(self):
        return reverse('mailings:notification_detail', args=[self.kwargs.get('pk')])

class NotificationDeleteView(LoginRequiredMixin, DeleteView):
    model = Notification
    success_url = reverse_lazy('mailings:notifications')

def finish_notification(request, pk):
    notification = Notification.objects.get(pk=pk)
    notification.status = 'f'
    notification.save()
    return redirect(request.META.get('HTTP_REFERER'))

class MessageListView(LoginRequiredMixin, ListView):
    model = Message

class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message

class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    fields = ('title', 'body',)

    def get_success_url(self):
        return reverse('mailings:message_detail', args=[self.kwargs.get('pk')])

class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    fields = ('title', 'body')
    success_url = reverse_lazy('mailings:messages')

class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('mailings:messages')


class ClientListView(LoginRequiredMixin, ListView):
    model = Client

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(owner=self.request.user)
        return qs


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    fields = ('name', 'email', 'comments',)
    success_url = reverse_lazy('mailings:clients')

    def form_valid(self, form):
        fields = form.save(commit=False)
        fields.owner = self.request.user
        fields.save()
        return super().form_valid(form)

class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    fields = ('name', 'email', 'comments',)

    def get_success_url(self):
        return reverse('mailings:client_detail', args=[self.kwargs.get('pk')])

class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('mailings:clients')

class AttemptListView(LoginRequiredMixin, ListView):
    model = NotificationAttempt




