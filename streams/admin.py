from django.contrib import admin
from .models import LiveStream, UserProfile
# Register your models here.
admin.site.register(LiveStream)
admin.site.register(UserProfile)