from django.conf import settings
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin  # разрешение, надо сделать авторизацию авторизацию
from django.contrib.messages.views import SuccessMessageMixin  # Миксин уведомления, отправляет сообщение в шаблон
from services.mixins import AuthorRequiredMixin  # Миксин редактирования статьи только автор
from .models import News, Category, Comment
from .forms import NewsCreateForm, NewsUpdateForm, CommentCreateForm



class NewsListViews(ListView):
    """ Список всех статей """
    model = News
    paginate_by = 9
    # template_name = 'blog/news_list.html'  # имя шаблона
    # template_name_suffix = '_update_form'  # добавить суфикс если такое имя есть
    # context_object_name = 'news_list'  # имя обьекта для перебора
    # extra_context = {'title' : 'Главная'} # почету то так не используют
    page_header = 'Блог Аркаши'
    page_title = 'Блог Аркаши'
    # queryset = News.objects.filter(is_published=True, category__is_published=True).select_related('category', 'created_by')
    queryset = model.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        """ GET:param object_list::param kwargs::return:"""
        context = super(NewsListViews, self).get_context_data(**kwargs)
        context['page_header'] = self.page_header
        context['page_title'] = self.page_title
        return context


class NewsByCategoryListView(ListView):
    '''
    представление для сортировки статей по категориям
    типа кликая на категорию попадаем в список отсоритрованный по этой категории
    '''
    # model = News                               #не нужна, так как пишем запрос сами
    paginate_by = 9
    category = None

    # template_name = 'blog/news_list.html'     # имя шаблона
    # context_object_name = 'news_list'         # имя обьекта для перебора
    def get_queryset(self):
        # достаем название категории слаг=слаг
        self.category = Category.objects.get(slug=self.kwargs['slug'])
        # вытащить категорию и ее дочении категории -   category__in=self.category.get_descendants(include_self=True)
        queryset = News.objects.filter(category__in=self.category.get_descendants(include_self=True))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.category.title
        context['page_header'] = f'Статьи из категории: {self.category.title}'
        return context


class NewsDetailViews(DetailView):
    """Детали статьи"""
    model = News
    queryset = model.objects.detail()

    def get_context_data(self, *, object_list=None, **kwargs):
        """ GET:param object_list::param kwargs::return:"""
        context = super(NewsDetailViews, self).get_context_data(**kwargs)
        # context['title'] = self.object.title     # получить заголовок, ЗАЧЕМ? если может из обьекта, не исплольз
        context['form'] = CommentCreateForm
        return context


class NewsCreateViews(LoginRequiredMixin, CreateView):
    model = News
    form_class = NewsCreateForm  # если б не использовали forms.py то надо прописать fields
    # fields = 'title', 'content', 'photo', ...              # используем NewsCreateForm
    # success_url = reverse_lazy('blog:news_list')           # без этого перенаправит на созданную статью
    # login_url = reverse_lazy("blog:news_request")          # куда перекинуть после авторизации, пропискано в настройках
    # template_name = 'blog/news_form.html'                  # форма по умолчанию
    page_header = 'Добавление новой записи'
    page_title = 'Добавление новой записи'

    def get_context_data(self, **kwargs):
        context = super(NewsCreateViews, self).get_context_data(**kwargs)
        context['page_header'] = self.page_header
        context['page_title'] = self.page_title
        return context

    def form_valid(self, form):
        '''В методе form_valid() валидируем нашу форму,
        а также сохраняем автором текущего пользователя на странице,
        которого получаем из запроса self.request.user'''
        form.instance.created_by = self.request.user
        form.save()
        return super().form_valid(form)


class NewsUpdateView(AuthorRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Представление: обновления материала на сайте
    """
    model = News
    form_class = NewsUpdateForm
    success_message = 'Материал был успешно обновлен'  # в шаблоне прописать {% if messages %} ...
    page_header = 'Обновление записи: '
    page_title = 'Обновление записи: '

    # template_name = 'blog/news_form.html'                  # форма по умолчанию

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['title'] = f'Обновление статьи: {self.object.title}'
        context['page_header'] = f'{self.page_header} {self.object.title}'
        context['page_title'] = f'{self.page_header} {self.object.title}'
        return context

    def form_valid(self, form):
        # form.instance.cre,,, = self.request.user # убрана для возможности получения пользователя для обновления
        form.save()
        return super().form_valid(form)


class NewsDeleteView(AuthorRequiredMixin, DeleteView):
    """
    Представление: удаления материала
    """
    model = News
    success_url = reverse_lazy('blog:news_list')
    # context_object_name = 'article'
    # template_name = 'blog/news_confirm_delete.html' # по дефолту
    page_header = 'Удаление записи: '
    page_title = 'Удаление записи: '

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_header'] = f'{self.page_header} {self.object.title}'
        context['page_title'] = f'{self.page_header} {self.object.title}'
        return context


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentCreateForm

    def is_ajax(self):
        return self.request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    def form_invalid(self, form):
        if self.is_ajax():
            return JsonResponse({'error': form.errors}, status=400)
        return super().form_invalid(form)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.news_id = self.kwargs.get('pk')
        comment.created_by = self.request.user
        comment.parent_id = form.cleaned_data.get('parent')
        comment.save()

        if self.is_ajax():
            return JsonResponse({
                'is_child': comment.is_child_node(),
                'id': comment.id,
                'created_by': comment.created_by.username,
                'parent_id': comment.parent_id,
                'time_create': comment.created_at.strftime('%Y-%b-%d %H:%M:%S'),
                'avatar': comment.created_by.profile.avatar.url,
                'content': comment.content,
                'get_absolute_url': comment.created_by.profile.get_absolute_url()
            }, status=200)

        return redirect(comment.news.get_absolute_url())
        #return redirect("blog:comment_create_view")

    def handle_no_permission(self):
        return JsonResponse({'error': 'Необходимо авторизоваться для добавления комментариев'}, status=400)


class HttpRequestPage(View):
    """Страница запросов.
    для тестов"""

    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            'request_resolver_match': request.resolver_match,
            'ipaddress': request.META['REMOTE_ADDR'],
            'meta': request.META,
            'request': request

        }
        return render(request, "blog/http_request_page.html", context=context)
