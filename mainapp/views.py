from django.shortcuts import render
from .models import Event  # если у тебя есть модель Event

def event_list(request):
    events = Event.objects.all()  # выбираем все события из базы
    return render(request, 'mainapp/event_list.html', {'events': events})
