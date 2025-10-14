import django.utils.datastructures
from django.shortcuts import render
from django.core.mail import send_mail
from decouple import config

from random import choice

from .forms import CreateCodeForm
from .models import UserVote, Higher, Lower


def winner(data):
    """Get teachers points and their names, sort them and return name, points and some message."""
    teacher_list = []
    for teacher in data:
        teacher_data = [teacher.points, teacher.name]
        teacher_list.append(teacher_data)
    # Sort list, since points is first, greater points would be first
    teacher_list.sort(reverse=True)
    # Since the actual teacher data is a list of two items, the names would be last i.e index 1
    # To get the name we refer to the index of the teacher on the main list and then the index of their name

    # These are outputs which would be returned
    # guard against index errors if there are less than three teachers
    if len(teacher_list) < 3:
        return "Not enough data", "", ""
    win = f"{teacher_list[0][1]} won with a total of {teacher_list[0][0]} points."
    runner = f"{teacher_list[1][1]} had {teacher_list[1][0]} points, as runner up."
    third = f"{teacher_list[2][1]} came third with {teacher_list[2][0]} points."

    return win, runner, third


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


# Function for index page
def home(request):
    context = {}
    return render(request, 'vote/index.html', context)


# Function to generate code for user and send them their code via email
# Also handles email checks and code retrieval in case the user lost their code
def code(request):
    # Would return the default page contents unless a post method is received
    if request.method == 'POST':
        # Users are expected to select a level (See code.html, line 15)
        selected_level = request.POST['level']
        # Calling form from forms.py
        form = CreateCodeForm(request.POST)

        # Check user email, selected level. Send them a new code if they are a student and unregistered
        # Reject their registration if their email is not a student email
        # Offer to resend code if they have already registered
        if form.is_valid():
            valid_levels = ['level 1', 'level 2', 'level 3']
            # Check if the selected level matches what we expect
            if selected_level in valid_levels:
                # Get the email from form after post
                try_email = form.cleaned_data['email']
                student_email = try_email
                # find email length
                email_length = len(student_email)
                position_count = 0  # holds position of tested charter in loop
                for char in student_email:  # loop to find the '@' in the email then tests from the @
                    if char == '@':  # when reaching the'@'....
                        # ...test if the rest of the string matches this, using list slicing
                        if student_email[position_count:email_length] == '@student.peterborough.ac.uk':
                            # If the email passes store
                            user_email = try_email
                        else:
                            # Else render error message
                            # Since rendering refreshes the page, no other process would run
                            context = {
                                'form': form,
                                'student': 'Sorry you are not a student',  # Expected by code.html line 25
                            }

                            return render(request, 'vote/code.html', context)
                    else:
                        # Would increase position_count if letter is not @ so it can be used for slicing
                        position_count += 1

                # We have two separate levels, so it can only be U or H
                if selected_level == 'level 1' or selected_level == 'level 2':
                    level = 'U'
                else:
                    level = 'H'
                # Call the code generator function, pass the letter which would be combined to the random numbers
                user_code = user_rand_code(level)

                try:
                    # Since user_email would only be available if the email passes check
                    # We watch for any errors, and check if email is stored on database
                    # On this occasion we want an error, an error means the email has not been registered
                    # No errors, then they are an existing user, so offer reset
                    registered_user = UserVote.objects.get(email=user_email)
                except UserVote.DoesNotExist:
                    # If the user is not registered, we can create a new user
                    save_user = UserVote(email=user_email, user_code=user_code)
                    save_user.save()

                    # Send the user their code via email
                    send_mail(
                        # The subject of the email
                        'College Voting Code',
                        # The body of the email
                        f'Hello, here is your code: {user_code}\nAs you are a {selected_level.title()} student, your code '
                        f'will only give you access to {selected_level.title()} teachers.\n\n'
                        f'Vote here: https://sleepy-sands-97119.herokuapp.com/voting/',
                        # The sending email
                        # README config is used to refer to an environmental variable (env)
                        # EMAIL_HOST_USER is an environmental variable which is set in the .env file
                        # This could easy be a string i.e 'example@gmail.com'
                        config('EMAIL_HOST_USER'),
                        # The receiving email
                        [user_email],
                        # Sends feedback once email fails to send
                        fail_silently=False
                    )

                    # Render the success page with the email
                    context = {
                        'email': user_email  # Expected by code.html line 25
                    }

                    return render(request, 'vote/success.html', context)

                # If the user is already registered, offer to resend code
                else:
                    context = {
                        'form': form,
                        'email': 'Email already registered.',
                        'reset': 'true',  # We set reset to true, code.html Line 28 expects this.
                    }
                    return render(request, 'vote/code.html', context)

            # Render error message if the selected level is not selected
            else:
                context = {
                    'form': form,
                    'message': 'Please select a level.',
                }
                return render(request, 'vote/code.html', context)

        try:
            # If user is already registered, we give them the option reset their code
            # It would be triggered by the resend code btn with reset as id (See code.html, line 29)
            reset = request.POST['reset']
        except django.utils.datastructures.MultiValueDictKeyError:
            # Django would throw an error if reset is not sent back during post
            # We just pass
            pass
        else:
            # The email field from forms.py, it has a field with email as tag
            reset_email = request.POST['email']
            # Check database for the reset email, this would return the id of the item in the database
            get_reset_user = UserVote.objects.get(email=reset_email)
            # Using the id, get the user_code field
            get_reset_user_code = get_reset_user.user_code

            # Send the user an email
            send_mail(
                'Resending Your Code',
                f'Hey there, you recently reset your code, here it is: {get_reset_user_code}\n'
                f'Vote for your teachers here: https://sleepy-sands-97119.herokuapp.com/voting/',
                config('EMAIL_HOST_USER'),
                [reset_email],
                fail_silently=False
            )

            # Still return the email form and a message
            # The message is expected on code.html as resent (See code.html, line 27)
            context = {
                'form': form,
                'resent': 'Code Successfully Sent!',
            }
            return render(request, 'vote/code.html', context)

    # If the request is not a post, render the form
    else:
        form = CreateCodeForm
    context = {
        'form': form
    }

    return render(request, 'vote/code.html', context)


# Function to handle the voting page
def voting(request):
    if request.method == 'POST':
        # Get teachers from their respective models
        h_teachers = Higher.objects.all()
        u_teachers = Lower.objects.all()
        try:
            # Get the code from the post request
            user_unique_code = request.POST['EUC']
            # Django would throw an error if EUC is not sent back during post
        except django.utils.datastructures.MultiValueDictKeyError:
            # If EUC is not sent, check for teachers
            try:
                selected_teacher = request.POST['teachers']
                # Django would throw an error if teachers is not sent back during post
            except django.utils.datastructures.MultiValueDictKeyError:
                # If neither EUC or teachers is sent, check for voted

                # README Basically, we are using one page for three different things
                # 1. Checking user code
                # 2. Rendering the relevant teachers, based on the selected level
                # 3. Rendering the voting page, based on the selected teacher.
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

    high_winner = winner(h_teachers)
    lower_winner = winner(u_teachers)

    context = {
        'u_teacher': u_teachers,
        'h_teacher': h_teachers,
        'total_votes': len(votes),
        'h_win': high_winner[0],
        'h_note': high_winner[1],
        'h_third': high_winner[2],
        'u_win': lower_winner[0],
        'u_note': lower_winner[1],
        'u_third': lower_winner[2],
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
