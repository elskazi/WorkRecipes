
from django.views.generic import DetailView, UpdateView, ListView, CreateView
from django.db import transaction
from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import UserPassesTestMixin                              # тест на изменение профиля
from django.contrib.auth.views import (PasswordChangeView, PasswordResetConfirmView,
                                       PasswordResetView )     # изм/восст пароля
from .models import Profile
from .forms import (UserUpdateForm, ProfileUpdateForm, UserRegisterForm, UserLoginForm,
                    UserPasswordChangeForm, UserForgotPasswordForm, UserSetNewPasswordForm)


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


class UserRegisterView(SuccessMessageMixin, CreateView):
    """
    Представление регистрации на сайте с формой регистрации
    """
    form_class = UserRegisterForm
    #success_url = reverse_lazy('home')
    template_name = 'system/user_register.html'
    success_message = 'Вы успешно зарегистрировались. Можете войти на сайт!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Регистрация на сайте'
        return context


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