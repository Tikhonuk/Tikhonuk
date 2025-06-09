from django.contrib import admin
from .models import Genre, Artist, Album, Composition, UserFavorites, Playlist

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)
    ordering = ('name',)
    verbose_name = "Жанр"
    verbose_name_plural = "Жанры"


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')
    search_fields = ('name', 'country')
    list_filter = ('country',)
    ordering = ('name',)
    list_display_links = ('name',)


class CompositionInline(admin.TabularInline):
    model = Composition
    extra = 0
    fields = ('title', 'genre', 'duration')
    readonly_fields = ('title',)  # если нужно readonly


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'release_date')
    search_fields = ('title', 'artist__name')
    list_filter = ('release_date', 'artist')
    date_hierarchy = 'release_date'
    ordering = ('release_date',)
    inlines = [CompositionInline]
    raw_id_fields = ('artist',)
    list_display_links = ('title',)


@admin.register(Composition)
class CompositionAdmin(admin.ModelAdmin):
    list_display = ('title', 'album', 'get_artist', 'genre', 'duration', 'created_at')
    search_fields = ('title', 'album__title', 'album__artist__name', 'genre__name')
    list_filter = ('genre', 'album__artist')
    ordering = ('title',)
    date_hierarchy = 'created_at'
    raw_id_fields = ('album', 'genre')
    list_display_links = ('title',)

    @admin.display(description='Исполнитель')
    def get_artist(self, obj):
        return obj.album.artist.name


@admin.register(UserFavorites)
class UserFavoritesAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'composition', 'added_at')
    search_fields = ('user_name', 'composition__title')
    list_filter = ('added_at',)
    date_hierarchy = 'added_at'
    raw_id_fields = ('composition',)
    readonly_fields = ('added_at',)


class CompositionInlineForPlaylist(admin.TabularInline):
    model = Playlist.compositions.through
    extra = 1
    verbose_name = "Композиция в плейлисте"
    verbose_name_plural = "Композиции в плейлисте"
    raw_id_fields = ('composition',)


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_compositions_count')
    search_fields = ('title',)
    inlines = [CompositionInlineForPlaylist]
    filter_horizontal = ('compositions',)
    list_display_links = ('title',)

    @admin.display(description='Количество композиций')
    def get_compositions_count(self, obj):
        return obj.compositions.count()
