from django.shortcuts import render, redirect, HttpResponse
from django.core.mail import send_mail

from random import choice

from .forms import CreateVoteForm
from .models import Vote

from .forms import CreateCodeForm
from .models import UserVote


def user_rand_code():
    letter_list = ['a', 'b', 'c', 'd']
    num_list = [1, 2, 3, 4, 5]
    spec_list = ['@', '?', '#']

    letter = choice(letter_list)
    num = choice(num_list)
    special = choice(spec_list)

    return f'{letter}{num}{special}'


def home(request):
    context = {}
    return render(request, 'vote/index.html', context)


def code(request):
    if request.method == 'POST':
        form = CreateCodeForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            user_code = user_rand_code()
            save_user = UserVote(email=user_email, user_code=user_code)
            save_user.save()

            send_mail(
                'College Voting Code',
                f'Hello, here is your code: {user_code}',
                'realdheetree@gmail.com',
                [user_email],
                fail_silently=False
            )

            return redirect('success')
    else:
        form = CreateCodeForm
    context = {
        'form': form
    }
    return render(request, 'vote/code.html', context)


def success(request):
    return render(request, 'vote/success.html')


def second_home(request):
    votes = Vote.objects.all()
    context = {
        'votes': votes
    }
    return render(request, 'vote/home.html', context)


def create(request):
    if request.method == 'POST':
        form = CreateVoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = CreateVoteForm()
    context = {
        'form': form
    }
    return render(request, 'vote/create.html', context)


def vote(request, vote_id):
    poll = Vote.objects.get(pk=vote_id)

    if request.method == 'POST':
        voted = request.POST['poll']
        if voted == 'option1':
            poll.option_one_count += 1
        elif voted == 'option2':
            poll.option_two_count += 1
        elif voted == 'option3':
            poll.option_three_count += 1
        else:
            return HttpResponse(400, 'Invalid form')

        poll.save()

        return redirect('results', vote_id)
    context = {
        'vote': poll
    }
    return render(request, 'vote/vote.html', context)


def results(request, vote_id):
    poll = Vote.objects.get(pk=vote_id)
    context = {
        'poll': poll
    }
    return render(request, 'vote/results.html', context)
