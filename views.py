from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count
from .models import Composition, UserFavorites, Genre
from .forms import CompositionForm  # позже сделаем форму
import random

def home(request):
    search_query = request.GET.get('q', '').strip()
    refresh_random = request.GET.get('refresh_random') == '1'

    if search_query:
        all_compositions = Composition.objects.filter(title__icontains=search_query)
    else:
        all_compositions = Composition.objects.all()

    popular_compositions = Composition.objects.annotate(
        favorites_count=Count('favorites')
    ).order_by('-favorites_count')[:5]

    latest_compositions = Composition.objects.order_by('-created_at')[:5]

    all_ids = list(Composition.objects.values_list('id', flat=True))
    random_compositions = Composition.objects.none()

    if all_ids:
        prev_random_ids = request.session.get('last_random_ids', [])

        if refresh_random:
            max_attempts = 10
            for _ in range(max_attempts):
                random_ids = random.sample(all_ids, min(len(all_ids), 5))
                if set(random_ids) != set(prev_random_ids):
                    break
            request.session['last_random_ids'] = random_ids
        else:
            random_ids = prev_random_ids
            if not random_ids:
                random_ids = random.sample(all_ids, min(len(all_ids), 5))
                request.session['last_random_ids'] = random_ids

        random_compositions = Composition.objects.filter(id__in=random_ids)

    genres_with_count = Genre.objects.annotate(
        composition_count=Count('composition')
    ).order_by('-composition_count')

    context = {
        'search_query': search_query,
        'all_compositions': all_compositions,
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


def composition_add(request):
    if request.method == 'POST':
        form = CompositionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('catalog:home')
    else:
        form = CompositionForm()
    return render(request, 'catalog/composition_form.html', {'form': form, 'title': 'Добавить композицию'})


def composition_edit(request, pk):
    composition = get_object_or_404(Composition, pk=pk)
    if request.method == 'POST':
        form = CompositionForm(request.POST, request.FILES, instance=composition)
        if form.is_valid():
            form.save()
            return redirect('catalog:composition_detail', pk=composition.pk)
    else:
        form = CompositionForm(instance=composition)
    return render(request, 'catalog/composition_form.html', {'form': form, 'title': 'Редактировать композицию'})


def composition_delete(request, pk):
    composition = get_object_or_404(Composition, pk=pk)
    if request.method == 'POST':
        composition.delete()
        return redirect('catalog:home')
    return render(request, 'catalog/composition_confirm_delete.html', {'composition': composition})
