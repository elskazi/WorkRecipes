from django.views.generic import DetailView, UpdateView, ListView, CreateView
from django.db import transaction
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin

from .models import Profile
from .forms import UserUpdateForm, ProfileUpdateForm, UserRegisterForm, UserLoginForm

                           # use model USER
"""
о get_user_model() по ссылке
# https://proghunter.ru/articles/django-base-2023-building-a-module-blog-and-model-articles-2
"""

class ProfileListView(ListView):
    #model = Profile
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
        context['title'] = f'Страница пользователя: {self.object.user.username}'
        return context


class ProfileUpdateView(UpdateView):
    """
    Представление для редактирования профиля
    """
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'system/profile_edit.html'

    def get_object(self, queryset=None):
        ''' В методе get_object() мы передаем текущего пользователя, чтобы не редактировать чужие профили.
        В контексте мы добавляем форму пользователя, где ссылаемся на текущего пользователя.'''
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Редактирование профиля пользователя: {self.request.user.username}'
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
        return reverse_lazy('profile_detail', kwargs={'slug': self.object.slug})


class UserRegisterView(SuccessMessageMixin, CreateView):
    """
    Представление регистрации на сайте с формой регистрации
    """
    form_class = UserRegisterForm
    success_url = reverse_lazy('home')
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
    next_page = reverse_lazy('system:profile_list')         # изменить  на профайл
    success_message = 'Добро пожаловать на сайт!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Авторизация на сайте'
        return context

class UserLogoutView(LogoutView):
    """
    Выход с сайта
    """
    next_page = reverse_lazy('blog:news_list')