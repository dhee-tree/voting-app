from django.forms import ModelForm
from .models import Vote
from .models import UserVote


class CreateVoteForm(ModelForm):
    class Meta:
        model = Vote
        fields = ['question', 'option_one', 'option_two', 'option_three']


class CreateCodeForm(ModelForm):
    class Meta:
        model = UserVote
        fields = ['email']
