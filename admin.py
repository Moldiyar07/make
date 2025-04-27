from django.contrib import admin
from .models import Project, Task

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'start_date', 'end_date', 'get_progress_percentage')
    list_filter = ('owner', 'start_date', 'end_date')
    search_fields = ('title', 'description')
    date_hierarchy = 'start_date'

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'assigned_to', 'deadline', 'status')
    list_filter = ('status', 'project', 'assigned_to')
    search_fields = ('title', 'description')
    date_hierarchy = 'deadline'
    raw_id_fields = ('project', 'assigned_to')

# Register your models here.
