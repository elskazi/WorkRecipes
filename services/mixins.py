from django.contrib.auth.mixins import AccessMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied


class AuthorRequiredMixin(AccessMixin):
    """
    Проверка Автора статьи или это стафф
    создали миксин наследуясь от основного AccessMixin и добавили возможность редактирования статьи только автору
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.is_authenticated:
            # Надо разрешить автору и Админу на правку Статьи, закоментировано то что было в обучении
            # if self.request.user != self.get_object().created_by or self.request.user.is_staff != True :
            #     messages.info(request, 'Изменение и удаление статьи доступно только автору')
            #     return redirect('blog:news_list')
            # return super().dispatch(request, *args, **kwargs)

            if request.user == self.get_object().created_by:
                return super().dispatch(request, *args, **kwargs)
            elif request.user.is_staff == True:
                return super().dispatch(request, *args, **kwargs)
            else:
                messages.info(request, 'Изменение и удаление статьи доступно только автору')
                # print(' не админ и не автор ')
                return redirect('blog:news_list')

        return redirect('blog:news_list')


class UserIsNotAuthenticated(UserPassesTestMixin):
    '''запрет регистрации авторизованных юзеров'''

    def test_func(self):
        if self.request.user.is_authenticated:
            messages.info(self.request, 'Вы уже авторизованы. Вы не можете посетить эту страницу.')
            raise PermissionDenied
            # return redirect('blog:news_list')
            # return redirect('blog:news_list')
        return True

    def handle_no_permission(self):
        return redirect('blog:news_list')
