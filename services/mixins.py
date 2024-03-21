from django.contrib.auth.mixins import AccessMixin
from django.contrib import messages
from django.shortcuts import redirect


class AuthorRequiredMixin(AccessMixin):
    """
    Проверка Автора статьи или это стафф
    создали миксин наследуясь от основного AccessMixin и добавили возможность редактирования статьи только автору
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.is_authenticated:
            if request.user != self.get_object().author or request.user.is_staff:
                messages.info(request, 'Изменение и удаление статьи доступно только автору')
                return redirect('blog:news_list')
        return super().dispatch(request, *args, **kwargs)