from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import News, Category
from .forms import NewsCreateForm, NewsUpdateForm

class NewsListViews(ListView):
    model = News
    paginate_by = 9

    # template_name = 'blog/news_list.html'  # имя шаблона
    # template_name_suffix = '_update_form'  # добавить суфикс если такое имя есть
    # context_object_name = 'news_list'  # имя обьекта для перебора
    # extra_context = {'title' : 'Главная'} # почету то так не используют
    page_header = 'Блог Аркаши'
    page_title = 'Блог Аркаши'
    queryset = News.objects.filter(is_published=True, category__is_published=True).select_related('category', 'created_by')

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
    #model = News
    paginate_by = 9
    category = None
    # template_name = 'blog/news_list.html'     # имя шаблона
    # context_object_name = 'news_list'         # имя обьекта для перебора
    def get_queryset(self):
        self.category = Category.objects.get(slug=self.kwargs['slug'])      # достаем название категории слаг=слаг
        #queryset_old = News.objects.all().filter(category__slug=self.category.slug, is_published=True)
        queryset = News.objects.filter(is_published=True, category__in=self.category.get_descendants(include_self=True), category__is_published=True).select_related('category', 'created_by')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.category.title
        context['page_header'] = f'Статьи из категории: {self.category.title}'
        return context


class NewsDetailViews(DetailView):
    """Детали статьи"""
    model = News

    def get_context_data(self, *, object_list=None, **kwargs):
        """ GET:param object_list::param kwargs::return:"""
        context = super(NewsDetailViews, self).get_context_data(**kwargs)
        #context['title'] = self.object.title     # получить заголовок, ЗАЧЕМ? если может из обьекта, не исплольз
        return context


class NewsCreateViews(CreateView):
    model = News
    #fields = 'title', 'content', 'photo', 'is_published', 'category', 'created_by' # используем NewsCreateForm
    form_class = NewsCreateForm
    #success_url = reverse_lazy('blog:news_list')           к# без этого перенаправит на созданную статью
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
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)


class NewsUpdateView(UpdateView):
    """
    Представление: обновления материала на сайте
    """
    model = News
    page_header = 'Обновление записи: '
    page_title = 'Обновление записи: '
    form_class = NewsUpdateForm
    #template_name = 'blog/articles_update.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['title'] = f'Обновление статьи: {self.object.title}'
        context['page_header'] = f'{self.page_header} {self.object.title}'
        context['page_title'] = f'{self.page_header} {self.object.title}'
        return context

    def form_valid(self, form):
        # form.instance.updater = self.request.user # убрана для возможности получения пользователя для обновления
        form.save()
        return super().form_valid(form)

class NewsDeleteView(DeleteView):
    """
    Представление: удаления материала
    """
    model = News
    success_url = reverse_lazy('blog:news_list')
    #context_object_name = 'article'
    #template_name = 'blog/news_confirm_delete.html' # по дефолту
    page_header = 'Удаление записи: '
    page_title = 'Удаление записи: '

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_header'] = f'{self.page_header} {self.object.title}'
        context['page_title'] = f'{self.page_header} {self.object.title}'
        return context


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



