import django.utils.datastructures
from django.shortcuts import render
from django.core.mail import send_mail
from decouple import config

from random import choice

from .forms import CreateCodeForm
from .models import UserVote, Higher, Lower


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

        try:
            reset = request.POST['reset']
        except django.utils.datastructures.MultiValueDictKeyError:
            pass
        else:
            reset_email = request.POST['email']
            get_reset_user = UserVote.objects.get(email=reset_email)
            get_reset_user_code = get_reset_user.user_code

            send_mail(
                'Resending Your Code',
                f'Hey there, you recently reset your code, here it is: {get_reset_user_code}\n'
                f'Vote for your teachers here: https://sleepy-sands-97119.herokuapp.com/voting/',
                config('EMAIL_HOST_USER'),
                [reset_email],
                fail_silently=False
            )

            context = {
                'form': form,
                'resent': 'Code Successfully Sent!',
            }
            return render(request, 'vote/code.html', context)

        if form.is_valid():
            valid_levels = ['level 1', 'level 2', 'level 3']
            if selected_level in valid_levels:
                try_email = form.cleaned_data['email']
                student_email = try_email  # Get email
                # find overall length, 27 chars long for '@student.peterborough.ac.uk'
                email_length = len(student_email)
                position_count = 0  # holds position of tested charter in loop
                for char in student_email:  # for loop to find the '@' in the email then tests that
                    if char == '@':  # when reaching the'@'....
                        # ...test if the rest of the string matches this
                        if student_email[position_count:email_length] == '@student.peterborough.ac.uk':
                            user_email = try_email
                        else:
                            context = {
                                'form': form,
                                'student': 'Sorry you are not a student',
                            }

                            return render(request, 'vote/code.html', context)
                    else:
                        position_count += 1

                if selected_level == 'level 1' or selected_level == 'level 2':
                    level = 'U'
                else:
                    level = 'H'
                user_code = user_rand_code(level)

                try:
                    registered_user = UserVote.objects.get(email=user_email)
                except UserVote.DoesNotExist:
                    save_user = UserVote(email=user_email, user_code=user_code)
                    save_user.save()

                    send_mail(
                        'College Voting Code',
                        f'Hello, here is your code: {user_code}\nAs you are a {selected_level.title()} student, your code '
                        f'will only give you access to {selected_level.title()} teachers.\n\n'
                        f'Vote here: https://sleepy-sands-97119.herokuapp.com/voting/',
                        config('EMAIL_HOST_USER'),
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
                        'email': 'Email already registered.',
                        'reset': 'true',
                    }
                    return render(request, 'vote/code.html', context)
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
        h_teachers = Higher.objects.all()
        u_teachers = Lower.objects.all()
        try:
            user_unique_code = request.POST['EUC']
        except django.utils.datastructures.MultiValueDictKeyError:
            try:
                selected_teacher = request.POST['teachers']
            except django.utils.datastructures.MultiValueDictKeyError:
                voted_teacher = request.POST['voted']
                glhpoint = request.POST['GLH']
                support = request.POST['support']
                style = request.POST['style']
                resources = request.POST['resources']
                teacher_type = request.POST['teacher_type']

                point = int(glhpoint) + int(support) + int(style) + int(resources)

                used_code = request.POST['code']
                context = {
                    'mode': 'voted',
                    'point': point,
                    'voted_teacher': voted_teacher
                }

                if teacher_type == "under":
                    get_teacher = Lower.objects.get(name=voted_teacher)
                if teacher_type == "higher":
                    get_teacher = Higher.objects.get(name=voted_teacher)

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
                teacher_type = request.POST['teacher_type']
                print(teacher_type)
                if teacher_type == "under":
                    teacher_obj = Lower.objects.get(name=selected_teacher)
                elif teacher_type == "higher":
                    teacher_obj = Higher.objects.get(name=selected_teacher)

                teacher_id = teacher_obj.id
                if teacher_type == "under":
                    obj = Lower.objects.get(id=teacher_id)
                    field = Lower
                    teacher_type = "under"
                elif teacher_type == "higher":
                    obj = Higher.objects.get(id=teacher_id)
                    field = Higher
                    teacher_type = "higher"

                print(teacher_id)

                units = ['unit_one', 'unit_two', 'unit_three', 'unit_four', 'unit_five']
                teacher_units = []
                for unit in units:
                    field_obj = field._meta.get_field(unit)
                    get_units = field_obj.value_from_object(obj)
                    # Do not add items that has None
                    if get_units != "None":
                        teacher_units.append(get_units)

                all_glh = obj.unit_one_glh + obj.unit_two_glh + obj.unit_three_glh + obj.unit_four_glh + obj.unit_five_glh
                averageglh = all_glh // 30

                context = {
                    'teacher': selected_teacher,
                    'mode': 'selected',
                    'units': teacher_units,
                    'object': obj,
                    'glhs': all_glh,
                    'aveGlhs': averageglh,
                    'user_code': user_code,
                    'teacher_type': teacher_type,
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
                    if "U" in user_unique_code:
                        teachers = u_teachers
                        teacher_type = "under"
                    elif "H" in user_unique_code:
                        teachers = h_teachers
                        teacher_type = "higher"
                    context = {
                        'message': user_unique_code,
                        'teachers': teachers,
                        'mode': 'start',
                        'teacher_type': teacher_type,
                    }
                    return render(request, 'vote/castVote.html', context)
    return render(request, 'vote/vote.html')


def result(request):
    u_teachers = Lower.objects.all()
    h_teachers = Higher.objects.all()
    votes = UserVote.objects.all()

    h_points = []
    for teacher in h_teachers:
        teacher_points = [teacher.points, teacher.name]
        h_points.append(teacher_points)
    h_points.sort(reverse=True)
    h_winner = h_points
    h_winner_note = f"{h_winner[0][1]} won with a total of {h_winner[0][0]} points."
    h_winner_diff = f"{h_winner[0][1]} had {h_winner[0][0] - h_winner[1][0]} points more than the runner up who had {h_winner[1][0]} points."

    context = {
        'u_teacher': u_teachers,
        'h_teacher': h_teachers,
        'total_votes': len(votes),
        'h_note': h_winner_note,
        'h_diff': h_winner_diff,
    }
    return render(request, 'vote/results.html', context)


def adminrest(request):
    if request.method == 'POST':
        action = request.POST['reset']
        print(action)
        counts = UserVote.objects.all()
        h_points = Higher.objects.all()
        u_points = Lower.objects.all()
        for reset in counts:
            reset.user_vote_count = 0
            reset.save()

        for reset in h_points:
            reset.points = 0
            reset.save()

        for reset in u_points:
            reset.points = 0
            reset.save()

    vote_counts = UserVote.objects.all()
    context = {
        'counts': vote_counts,
    }
    return render(request, 'vote/reset.html', context)
