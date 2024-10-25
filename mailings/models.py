
from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}
PERIOD = [('w', 'Раз в неделю'), ('d', 'Раз в день'), ('m', 'Раз в месяц')]
STATUS_ = [('f', 'Завершена'), ('c', 'Создана'), ('p', 'Запущена')]
# Create your models here.

class Client(models.Model):
    email = models.EmailField(verbose_name='контактный email')
    name = models.CharField(max_length=255, verbose_name='фио')
    comments = models.TextField(**NULLABLE, verbose_name='комментарий')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='чей клиент')

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'

    def __str__(self):
        return f'{self.name} - {self.email}'

class Message(models.Model):
    title = models.CharField(max_length=255, verbose_name='тема письма')
    body = models.TextField(verbose_name='тело письма')

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сooбщения'

    def __str__(self):
        return self.title

class Notification(models.Model):
    start_at = models.DateTimeField(verbose_name='дата начала отправки рассылки')
    finish_at = models.DateTimeField(verbose_name='дата окончания отправки рассылки')
    first_send_time = models.DateTimeField(verbose_name='дата и время первой отправки рассылки', **NULLABLE)
    period = models.CharField(max_length=1, choices=PERIOD, verbose_name='периодичность')
    status = models.CharField(default= 'c', max_length=1, choices=STATUS_, verbose_name='статус рассылки')
    client = models.ManyToManyField(Client, verbose_name='клиент', related_name='clients')
    creator = models.ForeignKey(User, verbose_name='автор', related_name='users', default=1, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='сообщение')
    last_send_time = models.DateTimeField(verbose_name='дата и время последней отправки рассылки', **NULLABLE)

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'
        permissions = [
            ('update_status', 'Может отключать рассылки'),
        ]

    def __str__(self):
        return f'{self.message}'

class NotificationAttempt(models.Model):
    last_attempt_at = models.DateTimeField(auto_now_add=True, verbose_name='время последней попытки')
    is_sent = models.BooleanField(default=False, verbose_name='статус попытки')
    server_message = models.TextField(**NULLABLE, verbose_name='ответ почтового сервера')
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, verbose_name='рассылка')

    class Meta:
        verbose_name = 'попытка рассылки'
        verbose_name_plural = 'попытки рассылки'

    def __str__(self):
        return f'{self.pk} - {self.is_sent}'





