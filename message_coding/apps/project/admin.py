from django.contrib import admin
import apps.project.models as project

admin.site.register(project.Project)
admin.site.register(project.Task)

