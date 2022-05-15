from django.forms import ModelForm
from .models import UserVote


class CreateCodeForm(ModelForm):
    class Meta:
        model = UserVote
        fields = ['email']
