from django.shortcuts import render, redirect, HttpResponse
from django.core.mail import send_mail

from random import choice

from .forms import CreateVoteForm
from .models import Vote

from .forms import CreateCodeForm
from .models import UserVote


def user_rand_code(level):
    num_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]

    num = choice(num_list)
    num2 = choice(num_list)
    num3 = choice(num_list)
    num4 = choice(num_list)
    num5 = choice(num_list)
    num6 = choice(num_list)

    return f'{level}-{num}{num2}{num3}{num4}{num5}{num6}'


def home(request):
    context = {}
    return render(request, 'vote/index.html', context)


def code(request):
    if request.method == 'POST':
        selected_level = request.POST['level']
        form = CreateCodeForm(request.POST)
        if form.is_valid():
            valid_levels = ['level 1', 'level 2', 'level 3']
            if selected_level in valid_levels:
                user_email = form.cleaned_data['email']

                if selected_level == 'level 1' or selected_level == 'level 2':
                    level = 'U'
                else:
                    level = 'H'
                user_code = user_rand_code(level)
                save_user = UserVote(email=user_email, user_code=user_code)
                # save_user.save()

                selected_level_title = selected_level.title()
                send_mail(
                    'College Voting Code',
                    f'Hello, here is your code: {user_code}\nAs you are a {selected_level_title} student, your code '
                    f'will only give you access to {selected_level_title} teachers.\n\n'
                    f'Vote here: https://sleepy-sands-97119.herokuapp.com/voting/',
                    'realdheetree@gmail.com',
                    [user_email],
                    fail_silently=False
                )

                context = {
                    'email': user_email
                }

                return render(request, 'vote/success.html', context)
            else:
                context = {
                    'form': form,
                    'message': 'Please select a level.',
                }
                return render(request, 'vote/code.html', context)
    else:
        form = CreateCodeForm
    context = {
        'form': form
    }
    return render(request, 'vote/code.html', context)


def voting(request):
    return render(request, 'vote/vote.html')


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
