from django.urls import path

from .views import ArticleDetailView, ArticleListView, CreateArticleView, UpdateArticleView, DeleteArticleView

app_name = 'blogapp'

urlpatterns = [
    path('', ArticleListView.as_view(), name='home'),
    path('articles/<int:pk>/', ArticleDetailView.as_view(), name='article'),
    path('articles/add/', CreateArticleView.as_view(), name='article_add'),
    path('articles/<int:pk>/edit/', UpdateArticleView.as_view(), name='article_update'),
    path('articles/<int:pk>/delete/', DeleteArticleView.as_view(), name='article_delete'),

]
