from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(blank=True, verbose_name='Содержимое поста')
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    author = models.ForeignKey(get_user_model(),
                               on_delete=models.SET_NULL,
                               related_name='articles',
                               null=True,
                               default=None
                               )

    def get_absolute_url(self):
        return reverse('blogapp:article', kwargs={'pk': self.pk})
