from django.contrib import admin
import message_coding.apps.coding.models as coding

admin.site.register(coding.Scheme)
admin.site.register(coding.CodeGroup)
admin.site.register(coding.Code)

