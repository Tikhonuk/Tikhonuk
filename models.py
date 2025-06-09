from django.db import models
from django.contrib.auth.models import User

class Genre(models.Model):
    name = models.CharField("Жанр", max_length=100, unique=True)

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.name


class Artist(models.Model):
    name = models.CharField("Имя артиста", max_length=200)
    country = models.CharField("Страна", max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = "Исполнитель"
        verbose_name_plural = "Исполнители"

    def __str__(self):
        return self.name


class Album(models.Model):
    title = models.CharField("Название альбома", max_length=200)
    artist = models.ForeignKey(Artist, verbose_name="Исполнитель", on_delete=models.CASCADE, related_name="albums")
    release_date = models.DateField("Дата выпуска", blank=True, null=True)

    class Meta:
        verbose_name = "Альбом"
        verbose_name_plural = "Альбомы"

    def __str__(self):
        return f"{self.title} — {self.artist.name}"


class Composition(models.Model):
    title = models.CharField("Название композиции", max_length=200)
    album = models.ForeignKey(Album, verbose_name="Альбом", on_delete=models.CASCADE, related_name="compositions")
    genre = models.ForeignKey(Genre, verbose_name="Жанр", on_delete=models.SET_NULL, null=True, blank=True)
    duration = models.DurationField("Длительность")
    audio_file = models.FileField("Аудиофайл", upload_to='audio_files/', null=True, blank=True)  # новое поле
    created_at = models.DateTimeField("Дата добавления", auto_now_add=True)

    class Meta:
        verbose_name = "Композиция"
        verbose_name_plural = "Композиции"

    def __str__(self):
        return self.title


class UserFavorites(models.Model):
    user_name = models.CharField("Имя пользователя", max_length=150)
    composition = models.ForeignKey(Composition, verbose_name="Композиция", on_delete=models.CASCADE, related_name="favorites")
    added_at = models.DateTimeField("Дата добавления в избранное", auto_now_add=True)

    class Meta:
        verbose_name = "Избранная композиция"
        verbose_name_plural = "Избранные композиции"

    def __str__(self):
        return f"{self.user_name} — {self.composition.title}"


class Playlist(models.Model):
    title = models.CharField("Название плейлиста", max_length=200)
    compositions = models.ManyToManyField(Composition, verbose_name="Композиции", related_name="playlists", blank=True)

    class Meta:
        verbose_name = "Плейлист"
        verbose_name_plural = "Плейлисты"

    def __str__(self):
        return self.title
