from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import News, Category


class NewsListViews(ListView):
    model = News
    paginate_by = 10
    # template_name = 'blog/news_list.html'  # имя шаблона
    # template_name_suffix = '_update_form'  # добавить суфикс если такое имя есть
    # context_object_name = 'news_list'  # имя обьекта для перебора
    # extra_context = {'title' : 'Главная'} # почету то так не используют
    page_header = '1 Список новостей'
    page_title = '2 Список новостей'
    queryset = News.objects.filter(archived=False).select_related('category')

    def get_context_data(self, *, object_list=None, **kwargs):
        """ GET:param object_list::param kwargs::return:"""
        context = super(NewsListViews, self).get_context_data(**kwargs)
        context['page_header'] = self.page_header
        context['page_title'] = self.page_title
        context['ipaddress'] = self.request.META['REMOTE_ADDR']
        return context


class NewsDetailViews(DetailView):
    model = News


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