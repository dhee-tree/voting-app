import django.utils.datastructures
from django.shortcuts import render
from django.core.mail import send_mail

from random import choice

from .forms import CreateCodeForm
from .models import UserVote, Higher


def user_rand_code(level):
    """Generates six random number, which would be combined with either H or U for user code."""
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
                save_user.save()

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
    if request.method == 'POST':
        teachers = Higher.objects.all()
        try:
            user_unique_code = request.POST['EUC']
            print(user_unique_code)
        except django.utils.datastructures.MultiValueDictKeyError:
            try:
                selected_teacher = request.POST['teachers']
            except django.utils.datastructures.MultiValueDictKeyError:
                status = request.POST['voted']
                glhpoint = request.POST['GLH']
                support = request.POST['support']
                style = request.POST['style']
                resources = request.POST['resources']

                point = int(glhpoint) + int(support) + int(style) + int(resources)

                used_code = request.POST['code']
                context = {
                    'mode': 'voted',
                    'point': point,
                    'voted_teacher': status
                }

                get_teacher = Higher.objects.get(name=status)
                old_point = get_teacher.points
                print(old_point)
                get_teacher.points = old_point + int(point)
                get_teacher.save()

                get_used_code = UserVote.objects.get(user_code=used_code)
                old_code_count = get_used_code.user_vote_count
                get_used_code.user_vote_count = old_code_count + 1
                get_used_code.save()
                return render(request, 'vote/castVote.html', context)

            else:
                user_code = request.POST['code']
                print(selected_teacher)
                teacher_obj = Higher.objects.get(name=selected_teacher)
                teacher_id = teacher_obj.id

                print(teacher_id)

                units = ['unit_one', 'unit_two', 'unit_three']
                teacher_units = []
                for unit in units:
                    obj = Higher.objects.get(id=teacher_id)
                    field_obj = Higher._meta.get_field(unit)
                    get_units = field_obj.value_from_object(obj)
                    teacher_units.append(get_units)

                all_glh = obj.unit_one_glh + obj.unit_two_glh + obj.unit_three_glh
                averageglh = all_glh // 60

                context = {
                    'teacher': selected_teacher,
                    'mode': 'selected',
                    'units': teacher_units,
                    'object': obj,
                    'glhs': all_glh,
                    'aveGlhs': averageglh,
                    'user_code': user_code,
                }
                return render(request, 'vote/castVote.html', context)
        else:
            try:
                stored_codes = UserVote.objects.get(user_code=user_unique_code)
                print(stored_codes.id)
            except UserVote.DoesNotExist:
                context = {
                    'message': 'Your code is not valid!'
                }
                return render(request, 'vote/vote.html', context)
            else:
                check_vote = stored_codes.user_vote_count
                if check_vote > 0:
                    context = {
                        'message': 'Your code has already being used to vote!'
                    }
                    return render(request, 'vote/vote.html', context)
                else:
                    context = {
                        'message': user_unique_code,
                        'teachers': teachers,
                        'mode': 'start',
                    }
                    return render(request, 'vote/castVote.html', context)
    return render(request, 'vote/vote.html')


def result(request):
    teachers = Higher.objects.all()
    context = {
        'teacher': teachers
    }
    return render(request, 'vote/results.html', context)

