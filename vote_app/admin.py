from django.contrib import admin
from .models import Vote, UserVote, Teachers

admin.site.register(Vote)
admin.site.register(UserVote)
admin.site.register(Teachers)
