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

        email = request.POST.get(
            'email',
            ''
        ).strip()

        password = request.POST.get(
            'password',
            ''
        )


        try:

            student = Login.objects.get(
                email=email,
                password=password
            )


            # Store student ID

            request.session[
                'student_id'
            ] = student.id


            return redirect(
                'dashboard'
            )


        except Login.DoesNotExist:

            return render(
                request,
                'login.html',
                {
                    'error':
                    'Invalid email or password.'
                }
            )


    return render(
        request,
        'login.html'
    )


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

    technologies = Technology.objects.all().order_by(
        'technology_name'
    )


    return render(

        request,

        'practice.html',

        {
            'technologies':
            technologies
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

    # Only POST allowed

    if request.method != 'POST':

        return redirect(
            'practice'
        )


    # -----------------------------------------
    # GET STUDENT
    # -----------------------------------------

    student_id = request.session.get(
        'student_id'
    )


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


    # -----------------------------------------
    # GET TECHNOLOGY
    # -----------------------------------------

    technology_id = request.POST.get(
        'technology_id'
    )


    if not technology_id:

        return redirect(
            'practice'
        )


    try:

        selected_technology = Technology.objects.get(

            id=technology_id

        )

    except Technology.DoesNotExist:

        return redirect(
            'practice'
        )


    # -----------------------------------------
    # GET QUESTIONS
    # -----------------------------------------

    questions = Question.objects.filter(

        technology=selected_technology

    ).order_by(

        'id'

    )


    total_questions = questions.count()


    # -----------------------------------------
    # CREATE RESULT FIRST
    # -----------------------------------------

    interview_result = Result.objects.create(

        student=student,

        technology=selected_technology,

        score=0,

        total_questions=total_questions,

        percentage=0

    )


    total_score = 0


    # -----------------------------------------
    # PROCESS EACH QUESTION
    # -----------------------------------------

    for question in questions:


        student_answer = request.POST.get(

            f'answer_{question.id}',

            ''

        ).strip()


        # -------------------------------------
        # CORRECT ANSWER
        # -------------------------------------

        correct_answer = (

            question.correct_answer or ''

        ).strip().lower()


        submitted_answer = (

            student_answer

        ).strip().lower()


        # -------------------------------------
        # CHECK ANSWER
        # -------------------------------------

        is_correct = False

        question_score = 0


        if (

            submitted_answer

            and correct_answer

        ):


            # Simple text matching

            if (

                correct_answer
                in submitted_answer

                or

                submitted_answer
                in correct_answer

            ):

                is_correct = True

                question_score = 1


        # Add score

        total_score += question_score


        # -------------------------------------
        # SAVE STUDENT ANSWER
        # -------------------------------------

        StudentAnswer.objects.create(

            result=interview_result,

            question=question,

            student_answer=student_answer,

            score=question_score,

            is_correct=is_correct

        )


    # -----------------------------------------
    # CALCULATE PERCENTAGE
    # -----------------------------------------

    if total_questions > 0:

        percentage = (

            total_score
            / total_questions

        ) * 100

    else:

        percentage = 0


    # -----------------------------------------
    # UPDATE RESULT
    # -----------------------------------------

    interview_result.score = (
        total_score
    )

    interview_result.percentage = (
        percentage
    )

    interview_result.save()


    # -----------------------------------------
    # GO TO DASHBOARD
    # -----------------------------------------

    return redirect(
        'dashboard'
    )


# =====================================================
# FEATURE
# =====================================================

def feature(request):

    return render(
        request,
        'feature.html'
    )