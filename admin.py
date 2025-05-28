from django.contrib import admin
from .models import Event, atexam

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date')
    search_fields = ('title',)


@admin.register(atexam)
class AtexamAdmin(admin.ModelAdmin):
    list_display = ('title', 'exam_date', 'created_at', 'is_public')  
    search_fields = ('title', 'users__email')  
    list_filter = (
        'is_public',  
        ('created_at', admin.DateFieldListFilter), 
    )
    date_hierarchy = 'exam_date'  
    filter_horizontal = ('users',) 