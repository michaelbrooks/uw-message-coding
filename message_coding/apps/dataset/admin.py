from django.contrib import admin
import apps.dataset.models as dataset

admin.site.register(dataset.Dataset)
admin.site.register(dataset.Selection)
admin.site.register(dataset.Message)

