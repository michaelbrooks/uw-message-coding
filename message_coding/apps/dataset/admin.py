from django.contrib import admin
import message_coding.apps.dataset.models as dataset

admin.site.register(dataset.Dataset)
admin.site.register(dataset.Selection)
admin.site.register(dataset.Message)

