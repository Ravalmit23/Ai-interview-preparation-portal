from django.shortcuts import render, redirect

from .models import (
    Login,
    Technology,
    Question,
    Result,
    StudentAnswer,
)


# =====================================================
# HOME
# =====================================================

def index(request):

    return render(
        request,
        'index.html'
    )


# =====================================================
# REGISTER
# =====================================================

def register(request):

    if request.method == 'POST':

        name = request.POST.get(
            'name',
            ''
        ).strip()

        email = request.POST.get(
            'email',
            ''
        ).strip()

        password = request.POST.get(
            'password',
            ''
        )


        # Check empty fields

        if not name or not email or not password:

            return render(
                request,
                'register.html',
                {
                    'error':
                    'Please fill all fields.'
                }
            )


        # Check existing email

        if Login.objects.filter(
            email=email
        ).exists():

            return render(
                request,
                'register.html',
                {
                    'error':
                    'Email already registered.'
                }
            )


        # Create student

        student = Login.objects.create(

            name=name,

            email=email,

            password=password
        )


        # Automatically login

        request.session[
            'student_id'
        ] = student.id


        return redirect(
            'dashboard'
        )


    return render(
        request,
        'register.html'
    )


# =====================================================
# LOGIN
# =====================================================
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        try:
            student = Login.objects.get(
                email=email,
                password=password
            )

            request.session['student_id'] = student.id
            request.session.save()

            return redirect('dashboard')

        except Login.DoesNotExist:
            return render(request, 'login.html', {
                'error': 'Invalid email or password.'
            })

    return render(request, 'login.html')

# =====================================================
# LOGIN2
# =====================================================

def login2(request):

    return redirect(
        'login'
    )


# =====================================================
# DASHBOARD
# =====================================================

def dashboard(request):

    student_id = request.session.get(
        'student_id'
    )


    # Student not logged in

    if not student_id:

        return redirect(
            'login'
        )


    try:

        student = Login.objects.get(
            id=student_id
        )

    except Login.DoesNotExist:

        request.session.flush()

        return redirect(
            'login'
        )


    # Get student's interview results

    results = Result.objects.filter(

        student=student

    ).select_related(

        'technology'

    ).prefetch_related(

        'answers__question'

    ).order_by(

        '-date'

    )


    return render(

        request,

        'dashboard.html',

        {
            'student': student,
            'results': results
        }

    )


# =====================================================
# PRACTICE
# =====================================================

def practice(request):
    student_id = request.session.get('student_id')

    # User is not logged in
    if not student_id:
        return redirect('login')

    try:
        Login.objects.get(id=student_id)
    except Login.DoesNotExist:
        request.session.flush()
        return redirect('login')

    technologies = Technology.objects.all().order_by(
        'technology_name'
    )

    return render(
        request,
        'practice.html',
        {
            'technologies': technologies
        }
    )
# =====================================================
# TECHNOLOGY / INTERVIEW
# =====================================================

def technology_view(
    request,
    technology
):

    try:

        selected_technology = Technology.objects.get(

            technology_name__iexact=technology

        )

    except Technology.DoesNotExist:

        return redirect(
            'practice'
        )


    # Get questions belonging
    # to selected technology

    questions = Question.objects.filter(

        technology=selected_technology

    ).order_by(

        'id'

    )


    return render(

        request,

        'interview.html',

        {
            'technology':
            selected_technology,

            'questions':
            questions
        }

    )


# =====================================================
# SUBMIT INTERVIEW
# =====================================================

def submit_answer(request):
    if request.method != 'POST':
        return redirect('practice')

    student_id = request.session.get('student_id')

    if not student_id:
        return redirect('login')

    try:
        student = Login.objects.get(id=student_id)
    except Login.DoesNotExist:
        request.session.flush()
        return redirect('login')

    technology_id = request.POST.get('technology_id')

    if not technology_id:
        return redirect('practice')

    try:
        selected_technology = Technology.objects.get(
            id=technology_id
        )
    except Technology.DoesNotExist:
        return redirect('practice')

    questions = Question.objects.filter(
        technology=selected_technology
    ).order_by('id')

    total_questions = questions.count()

    interview_result = Result.objects.create(
        student=student,
        technology=selected_technology,
        score=0,
        total_questions=total_questions,
        percentage=0
    )

    total_percentage = 0

    for question in questions:

        student_answer = request.POST.get(
            f'answer_{question.id}',
            ''
        ).strip()

        correct_answer = (
            question.correct_answer or ''
        ).strip().lower()

        submitted_answer = student_answer.lower()

        question_percentage = 0

        if submitted_answer and correct_answer:

            # Convert answers into words
            correct_words = set(
                correct_answer.replace(
                    ',', ' '
                ).replace(
                    '.', ' '
                ).split()
            )

            submitted_words = set(
                submitted_answer.replace(
                    ',', ' '
                ).replace(
                    '.', ' '
                ).split()
            )

            # Remove very common words
            stop_words = {
                'the',
                'is',
                'a',
                'an',
                'and',
                'or',
                'to',
                'of',
                'in',
                'for',
                'with',
                'on',
                'it',
                'this',
                'that',
                'are',
                'was',
                'be',
                'as'
            }

            correct_words -= stop_words
            submitted_words -= stop_words

            if correct_words:

                matched_words = (
                    correct_words &
                    submitted_words
                )

                match_percentage = (
                    len(matched_words) /
                    len(correct_words)
                ) * 100

                question_percentage = round(
                    match_percentage
                )

                # Maximum 100%
                if question_percentage > 100:
                    question_percentage = 100

            # Exact answer
            if submitted_answer == correct_answer:
                question_percentage = 100

        # Consider 50%+ as correct
        is_correct = question_percentage >= 50

        total_percentage += question_percentage

        StudentAnswer.objects.create(
            result=interview_result,
            question=question,
            student_answer=student_answer,
            score=question_percentage,
            is_correct=is_correct
        )

    # Calculate overall percentage
    if total_questions > 0:
        overall_percentage = (
            total_percentage /
            total_questions
        )
    else:
        overall_percentage = 0

    interview_result.score = round(
        total_percentage
    )

    interview_result.percentage = round(
        overall_percentage,
        2
    )

    interview_result.save()

    return redirect('dashboard')
# =====================================================
# FEATURE
# =====================================================

def feature(request):

    return render(
        request,
        'feature.html'
    )

def logout_view(request):
    request.session.flush()
    return redirect('login')