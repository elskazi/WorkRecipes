from django.db import models
from django.contrib.auth import get_user_model  # model user
from django.core.validators import FileExtensionValidator # проверка изобраения
from django.urls import reverse
from datetime import date, timedelta
from django.db.models.signals import post_save      # сигналы
from django.dispatch import receiver                # сигналы
from django_resized import ResizedImageField        # resizer image


from services.utils import unique_slugify

User = get_user_model()


def avater_dir_path(instanse: 'User', filename: str) -> str :
    return 'user/{pk}_{username}/{filename}'.format(
        pk= instanse.user.pk,
        username = instanse.user.username,
        filename = filename,
    )

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(verbose_name='URL', max_length=255, blank=True, unique=True)
    avatar = ResizedImageField(size=[230, 230],
                               crop=['middle', 'center'],
                               verbose_name='Аватар',
                               upload_to=avater_dir_path,
                               #default='avatars/default.png',
                               blank=True,
                               null=True,
                               validators=[FileExtensionValidator(allowed_extensions=('png', 'jpg', 'jpeg'))])
    bio = models.TextField(max_length=500, blank=True, verbose_name='Информация о себе')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Дата рождения')

    @property
    def get_avatar(self):
        '''
        если нет аватарки то используем сайт для генерации аватарок
        В шаблоне профиля вызывать аватарку через {{ profile.get_avatar }}, вместо {{ profile.avatar.url }}.
        '''
        if self.avatar:
            return self.avatar.url
        return f'https://ui-avatars.com/api/?size=150&background=random&name={self.slug}'

    class Meta:
        """
        Сортировка, название таблицы в базе данных
        """
        ordering = ('user',)
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def save(self, *args, **kwargs):
        """
        Сохранение полей модели при их отсутствии заполнения
        """
        if not self.slug:
            self.slug = unique_slugify(self, self.user.username)
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Возвращение строки
        """
        return self.user.username

    def get_absolute_url(self):
        """
        Ссылка на профиль
        """
        return reverse('system:profile_detail', kwargs={'slug': self.slug})

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class Feedback(models.Model):
    """
    Модель обратной связи
    """
    subject = models.CharField(max_length=255, verbose_name='Тема письма')
    email = models.EmailField(max_length=255, verbose_name='Электронный адрес (email)')
    content = models.TextField(verbose_name='Содержимое письма')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки')
    ip_address = models.GenericIPAddressField(verbose_name='IP отправителя',  blank=True, null=True)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратная связь'
        ordering = ['-created_at']

    def __str__(self):
        return f'Вам письмо от {self.email}'