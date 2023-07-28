from django.contrib import admin

from .models import *


class ProjectAdmin(admin.ModelAdmin):
    list_display = ["title", "global_priory", "category", "is_published"]
    search_fields = ["title", "global_priory", "category.title"]
    list_editable = ["is_published"]


admin.site.register(Project, ProjectAdmin)
admin.site.register(StudySource)
admin.site.register(Category)