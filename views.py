from django.shortcuts import render, get_object_or_404
from .models import Composition, UserFavorites, Genre
from django.db.models import Count
import random

def home(request):
    search_query = request.GET.get('q', '').strip()  # Получаем поисковый запрос из GET параметров
    refresh_random = request.GET.get('refresh_random') == '1'  # Проверяем, была ли нажата кнопка "Обновить"

    # Все композиции с фильтром поиска, если есть
    if search_query:
        all_compositions = Composition.objects.filter(title__icontains=search_query)
    else:
        all_compositions = Composition.objects.all()

    # Популярные композиции: топ 5 по количеству избранных
    popular_compositions = Composition.objects.annotate(
        favorites_count=Count('favorites')
    ).order_by('-favorites_count')[:5]

    # Новые композиции: последние добавленные, топ 5
    latest_compositions = Composition.objects.order_by('-created_at')[:5]

    # Случайные композиции
    all_ids = list(Composition.objects.values_list('id', flat=True))
    random_compositions = Composition.objects.none()

    if all_ids:
        prev_random_ids = request.session.get('last_random_ids', [])

        if refresh_random:
            # Генерируем новые random_ids, отличающиеся от предыдущих (если возможно)
            max_attempts = 10
            for attempt in range(max_attempts):
                random_ids = random.sample(all_ids, min(len(all_ids), 5))
                if set(random_ids) != set(prev_random_ids):
                    break  # Нашли новые
            request.session['last_random_ids'] = random_ids
        else:
            # Используем предыдущие random_ids или генерируем при первом заходе
            random_ids = prev_random_ids
            if not random_ids:
                random_ids = random.sample(all_ids, min(len(all_ids), 5))
                request.session['last_random_ids'] = random_ids

        random_compositions = Composition.objects.filter(id__in=random_ids)

    # Жанры с количеством композиций (можно не использовать)
    genres_with_count = Genre.objects.annotate(
        composition_count=Count('composition')
    ).order_by('-composition_count')

    context = {
        'search_query': search_query,
        'all_compositions': all_compositions,  # Результаты поиска (или все, если поиска нет)
        'popular_compositions': popular_compositions,
        'latest_compositions': latest_compositions,
        'random_compositions': random_compositions,
        'genres_with_count': genres_with_count,
    }

    return render(request, 'catalog/home.html', context)


def composition_detail(request, pk):
    composition = get_object_or_404(Composition, pk=pk)
    context = {
        'composition': composition
    }
    return render(request, 'catalog/composition_detail.html', context)
