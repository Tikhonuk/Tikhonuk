from django.db import models
from django.contrib.auth.models import User  # встроенная модель пользователя


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.DateField()

    def __str__(self):
        return self.title


class atexam(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название экзамена")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания записи")
    exam_date = models.DateField(verbose_name="Дата проведения экзамена")
    image = models.ImageField(upload_to='exam_images/', null=True, blank=True, verbose_name="Изображение задания")
    users = models.ManyToManyField(User, verbose_name="Пользователи, пишущие экзамен")
    is_public = models.BooleanField(default=False, verbose_name="Опубликовано")

    def __str__(self):
        return self.title
