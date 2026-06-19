from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class CustomUser(AbstractUser):
    full_name = models.CharField('ФИО', max_length=150)
    birth_date = models.DateField('Дата рождения', null=True, blank=True)
    phone = models.CharField('Телефон', max_length=20)
    email = models.EmailField('E-mail', unique=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.full_name


class Application(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('learning', 'Идет обучение'),
        ('done', 'Обучение завершено'),
    ]
    TRANSPORT_CHOICES = [
        ('bus', 'Автобус'),
        ('electric', 'Электробус'),
        ('tram', 'Трамвай'),
    ]
    PAYMENT_CHOICES = [
        ('cash', 'Наличные'),
        ('card', 'Карта'),
        ('invoice', 'Безнал'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    transport = models.CharField(
        'Вид транспорта',
        max_length=20,
        choices=TRANSPORT_CHOICES
    )
    start_date = models.DateField('Дата начала обучения')
    payment = models.CharField(
        'Способ оплаты',
        max_length=20,
        choices=PAYMENT_CHOICES
    )
    status = models.CharField(
        'Статус',
        max_length=20,
        choices=STATUS_CHOICES,
        default='new'
    )
    created_at = models.DateTimeField('Создано', auto_now_add=True)

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.full_name} — {self.get_transport_display()}'

class Review(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        verbose_name='Заявка',
        related_name='reviews'
    )
    text = models.TextField('Текст отзыва')
    created_at = models.DateTimeField('Создано', auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']

    def __str__(self):
        return f'Отзыв от {self.user.full_name}'