from django.contrib import admin
import apps.coding.models as coding

admin.site.register(coding.Scheme)
admin.site.register(coding.SchemeVersion)
admin.site.register(coding.CodeGroup)
admin.site.register(coding.Code)