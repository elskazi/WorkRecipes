from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import News, Category



class NewsListViews(ListView):
    model = News
    paginate_by = 10
    # template_name = 'blog/news_list.html'  # имя шаблона
    # template_name_suffix = '_update_form'  # добавить суфикс если такое имя есть
    # context_object_name = 'news_list'  # имя обьекта для перебора
    # extra_context = {'title' : 'Главная'} # почету то так не используют
    page_header = 'Блог'
    page_title = 'Блог'
    page_default_img = f'{settings.STATIC_URL}BestCow800x450.jpg'
    queryset = News.objects.filter(is_published=True).select_related('category').select_related('created_by')

    def get_context_data(self, *, object_list=None, **kwargs):
        """ GET:param object_list::param kwargs::return:"""
        context = super(NewsListViews, self).get_context_data(**kwargs)
        context['page_header'] = self.page_header
        context['page_title'] = self.page_title
        context['ipaddress'] = self.request.META['REMOTE_ADDR']
        context['page_default_img'] = self.page_default_img
        return context


class NewsDetailViews(DetailView):
    model = News
    page_default_img = f'{settings.STATIC_URL}BestCow800x450.jpg'
    def get_context_data(self, *, object_list=None, **kwargs):
        """ GET:param object_list::param kwargs::return:"""
        context = super(NewsDetailViews, self).get_context_data(**kwargs)
        context['page_default_img'] = self.page_default_img
        return context


class NewsCreateViews(CreateView):
    model = News
    fields = 'title', 'content', 'photo', 'is_published', 'category', 'created_by'
    success_url = reverse_lazy('blog:news_list')
    page_header = 'Новая запись'
    page_title = 'Новая запись'

    def get_context_data(self, **kwargs):
        context = super(NewsCreateViews, self).get_context_data(**kwargs)
        context['page_header'] = self.page_header
        context['page_title'] = self.page_title
        return context

class HttpRequestPage(View):
    def get(self, request: HttpRequest) -> HttpResponse:

        request_resolver_match = request.resolver_match
        context = {
            'request_resolver_match': request_resolver_match,

        }
        return render(request, "blog/http_request_page.html", context=context)