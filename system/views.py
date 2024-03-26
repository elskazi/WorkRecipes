from django.views.generic import DetailView, UpdateView, ListView, CreateView, View, TemplateView
from django.db import transaction  # для обьедения форм при регитрации
from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import LoginView, LogoutView  # вход выход
from django.contrib.auth.tokens import default_token_generator  # подтвеждение емайла
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  # подтвеждение емайла
from django.utils.encoding import force_bytes  # подтвеждение емайла
from django.contrib.sites.models import Site  # подтвеждение емайла
from django.core.mail import send_mail  # подтвеждение емайла
from django.contrib.auth import login  # подтвеждение емайла
from django.shortcuts import redirect

from django.contrib.messages.views import SuccessMessageMixin  # Messages
from django.contrib.auth.mixins import UserPassesTestMixin  # тест на изменение профиля
from django.contrib.auth.views import (PasswordChangeView, PasswordResetConfirmView,
                                       PasswordResetView)  # изм/восст пароля
from .models import Profile, Feedback
from .forms import (UserUpdateForm, ProfileUpdateForm, UserRegisterForm, UserLoginForm,
                    UserPasswordChangeForm, UserForgotPasswordForm, UserSetNewPasswordForm,
                    FeedbackCreateForm, )

from services.mixins import UserIsNotAuthenticated  # запрет регистрации авторизованных юзеров
from services.email import send_contact_email_message # отрпавка письма Админу
from services.utils import get_client_ip  # получение IP

from django.contrib.auth import get_user_model  # model User, нужен для подтвеждение емайла

User = get_user_model()


class ProfileListView(ListView):
    """
    Представление для  списка профилей
    """
    # model = Profile
    template_name = 'system/profile_list.html'
    queryset = Profile.objects.all().select_related('user')


class ProfileDetailView(DetailView):
    """
    Представление для просмотра профиля
    """
    model = Profile
    context_object_name = 'profile'
    template_name = 'system/profile_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'Страница пользователя: {self.object.user.username}'
        return context


class ProfileUpdateView(UserPassesTestMixin, UpdateView):
    """
    Представление для редактирования профиля
    """
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'system/profile_edit.html'

    # def get_object(self, queryset=None):
    #     ''' В методе get_object() мы передаем текущего пользователя, чтобы не редактировать чужие профили.
    #     В контексте мы добавляем форму пользователя, где ссылаемся на текущего пользователя.'''
    #     return self.request.user.profile

    def test_func(self):
        # проверяем вначале юзер авторизован или нет
        if self.request.user.is_authenticated:
            # проверяет это стаф или текущий юзер (для редактирования профиля) /user/NAME/NOT self.user = 403
            if self.request.user.is_staff or self.request.user.profile.slug == self.get_object().slug:
                return True
            else:
                return False
        else:
            return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'Редактирование профиля пользователя: {self.request.user.username}'
        if self.request.POST:
            context['user_form'] = UserUpdateForm(self.request.POST, instance=self.request.user)
        else:
            context['user_form'] = UserUpdateForm(instance=self.request.user)
        return context

    def form_valid(self, form):
        '''В методе form_valid() мы используем transaction.atomic, для корректного сохранения данных двух форм в нашей БД.'''
        context = self.get_context_data()
        user_form = context['user_form']
        with transaction.atomic():
            if all([form.is_valid(), user_form.is_valid()]):
                user_form.save()
                form.save()
            else:
                context.update({'user_form': user_form})
                return self.render_to_response(context)
        return super(ProfileUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('system:profile_detail', kwargs={'slug': self.object.slug})


class UserRegisterView(UserIsNotAuthenticated, SuccessMessageMixin, CreateView):
    """
    Представление регистрации на сайте с формой регистрации, и отправкой письма подтвеждения
    """
    form_class = UserRegisterForm
    # success_url = reverse_lazy('blog:news_list')
    template_name = 'system/registration/user_register.html'
    success_message = 'Письмо подтверждения отправлено!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Регистрация на сайте'
        return context

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        # Функционал для отправки письма и генерации токена
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        activation_url = reverse_lazy('system:confirm_email', kwargs={'uidb64': uid, 'token': token})
        current_site = Site.objects.get_current().domain
        send_mail(
            'Подтвердите свой электронный адрес',
            f'Пожалуйста, перейдите по следующей ссылке, чтобы подтвердить свой адрес электронной почты: http://{current_site}{activation_url}',
            'elskazii@yandex.ru',
            [user.email],
            fail_silently=False,
        )
        return redirect('system:email_confirmation_sent')


class UserLoginView(SuccessMessageMixin, LoginView):
    """
    Авторизация на сайте
    """
    form_class = UserLoginForm
    template_name = 'system/user_login.html'
    next_page = reverse_lazy('blog:news_list')  # изменить  на профайл
    success_message = 'Добро пожаловать на сайт!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Авторизация на сайте'
        return context


class UserLogoutView(SuccessMessageMixin, LogoutView):
    """
    Выход с сайта
    """
    next_page = reverse_lazy('blog:news_list')
    success_message = 'Вы вышли из учётной записи.'


# далее игра с паролями
class UserPasswordChangeView(SuccessMessageMixin, PasswordChangeView):
    """
    Изменение пароля пользователя (когда уже сделана авторизация)
    """
    form_class = UserPasswordChangeForm
    template_name = 'system/user_password_change.html'
    success_message = 'Ваш пароль был успешно изменён!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Изменение пароля на сайте'
        return context

    def get_success_url(self):
        return reverse_lazy('system:profile_detail', kwargs={'slug': self.request.user.profile.slug})


class UserForgotPasswordView(SuccessMessageMixin, PasswordResetView):
    """
    Представление по сбросу пароля по почте
    """
    form_class = UserForgotPasswordForm
    template_name = 'system/user_password_reset.html'
    success_url = reverse_lazy('blog:news_list')
    success_message = 'Письмо с инструкцией по восстановлению пароля отправлена на ваш email'
    subject_template_name = 'system/email/password_subject_reset_mail.txt'
    email_template_name = 'system/email/password_reset_mail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Запрос на восстановление пароля'
        return context


class UserPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
    """
    Представление установки нового пароля (из почты)
    """
    form_class = UserSetNewPasswordForm
    template_name = 'system/user_password_set_new.html'
    success_url = reverse_lazy('blog:news_list')
    success_message = 'Пароль успешно изменен. Можете авторизоваться на сайте.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Установить новый пароль'
        return context


# далее подтвеждение почты
class UserConfirmEmailView(View):
    '''
    Перекидывает и проверяет из отправленного письма, в это представление
    если все ок то перекинуть на страницу email_confirmed, если нет то на стр email_confirmation_failed
    '''

    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('system:email_confirmed')
        else:
            return redirect('system:email_confirmation_failed')


class EmailConfirmationSentView(TemplateView):
    '''Письмо подтверждения отправлено!  перекидывает Юзера на эту страницу, после регитрации'''
    template_name = 'system/registration/email_confirmation_sent.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Письмо активации отправлено'
        return context


class EmailConfirmedView(TemplateView):
    '''Электронная почта подтверждена '''
    template_name = 'system/registration/email_confirmed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Ваш электронный адрес активирован'
        return context


class EmailConfirmationFailedView(TemplateView):
    '''Ошибка подтверждения по электронной почте, типа если ранее уже подтвердил '''
    template_name = 'system/registration/email_confirmation_failed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Ваш электронный адрес не активирован'
        return context


# Обратная связь
class FeedbackCreateView(SuccessMessageMixin, CreateView):
    model = Feedback
    form_class = FeedbackCreateForm
    success_message = 'Ваше письмо успешно отправлено администрации сайта'
    template_name = 'system/feedback.html'
    extra_context = {'title': 'Контактная форма'}
    success_url = reverse_lazy('blog:news_list')

    def form_valid(self, form):
        """
        Метод form_valid() переопределяет метод родительского класса и вызывается после успешной валидации формы.
        В нем создается объект feedback, заполняется его атрибут ip_address с помощью функции get_client_ip(),
        а если пользователь аутентифицирован, то заполняется его атрибут user.
        Затем вызывается функция send_contact_email_message(), которая отправляет электронное письмо.
        """
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.ip_address = get_client_ip(self.request)
            if self.request.user.is_authenticated:
                feedback.user = self.request.user
            send_contact_email_message(feedback.subject, feedback.email, feedback.content, feedback.ip_address,
                                       feedback.user_id)
        return super().form_valid(form)
