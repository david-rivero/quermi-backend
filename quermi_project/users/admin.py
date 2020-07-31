from django.contrib import admin
from .models import QuermiProfileUser, ProfileLanguage, ProfileServices

admin.site.register(QuermiProfileUser)
admin.site.register(ProfileServices)
admin.site.register(ProfileLanguage)