from django.contrib import admin
from .models import Vote, UserVote

admin.site.register(Vote)
admin.site.register(UserVote)
