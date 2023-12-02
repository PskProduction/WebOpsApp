from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from blogapp.models import Article


class ArticleListView(ListView):
    model = Article
    template_name = 'blogapp/articles-list.html'
    context_object_name = 'articles'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related('author')
        queryset = queryset.defer('content')

        return queryset


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blogapp/article-detail.html'


class CreateArticleView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = 'blogapp/article-create.html'
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdateArticleView(LoginRequiredMixin, UpdateView):
    model = Article
    template_name = 'blogapp/article-update.html'
    fields = ['title', 'content']

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        user = self.request.user
        if user == self.object.author or user.is_staff:
            self.object.update()
            return redirect(request.META["HTTP_REFERER"])


class DeleteArticleView(LoginRequiredMixin, DeleteView):
    model = Article
    success_url = reverse_lazy('blogapp:home')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        user = self.request.user
        if user == self.object.author or user.is_staff:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
