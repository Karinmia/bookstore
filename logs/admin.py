from django.contrib import admin
from .models import HttpLog, CRUDLog

admin.site.register(HttpLog)
admin.site.register(CRUDLog)
