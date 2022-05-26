from django.contrib import admin
from .models import UserVote, Higher, Lower

admin.site.register(UserVote)
admin.site.register(Higher)
admin.site.register(Lower)
