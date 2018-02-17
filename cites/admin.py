from django.contrib import admin

from .models import Paragraph, Story

admin.site.register(Story)
admin.site.register(Paragraph)
