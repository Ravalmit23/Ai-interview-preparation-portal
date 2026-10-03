from django.db import models
from django.db import models
from django.utils import timezone

# =====================================================
# STUDENT / USER
# =====================================================

class Login(models.Model):

    name = models.CharField(
        max_length=100,
        default=''
    )

    email = models.EmailField(
        unique=True
    )

    password = models.CharField(
        max_length=128
    )

    def __str__(self):
        return self.name or self.email


# =====================================================
# TECHNOLOGY
# =====================================================

class Technology(models.Model):
    technology_name = models.CharField(
        max_length=100,
        unique=True,
        null=True,
        blank=True
    )

    category = models.CharField(
        max_length=100,
        blank=True
    )

    total_questions = models.IntegerField(default=0)

    duration = models.IntegerField(default=30)

    def __str__(self):
        return self.technology_name or "Unnamed Technology"


# =====================================================
# QUESTION
# =====================================================

class Question(models.Model):

    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    ]

    technology = models.ForeignKey(
        Technology,
        on_delete=models.CASCADE,
        related_name='questions'
    )

    question_text = models.TextField()

    category = models.CharField(
        max_length=100,
        blank=True
    )

    difficulty = models.CharField(
        max_length=20,
        choices=DIFFICULTY_CHOICES,
        default='Easy'
    )

    correct_answer = models.TextField(
        blank=True
    )

    def __str__(self):
        return self.question_text


# =====================================================
# RESULT
# =====================================================

class Result(models.Model):
    student = models.ForeignKey(
        Login,
        on_delete=models.CASCADE,
        related_name='results',
        null=True,
        blank=True
    )

    technology = models.ForeignKey(
        Technology,
        on_delete=models.CASCADE,
        related_name='results',
        db_column='technology'
    )

    score = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=0)
    percentage = models.FloatField(default=0)

    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return (
            f"{self.student.name if self.student else 'Unknown'} - "
            f"{self.technology.technology_name if self.technology else 'Unknown Technology'}"
        )
    def __str__(self):
        student_name = self.student.name if self.student else "Unknown Student"

        return (
            f"{student_name} - "
            f"{self.technology.technology_name}"
        )    
    def __str__(self):
        return (
            f"{self.student.name} - "
            f"{self.technology.technology_name}"
        )


# =====================================================
# STUDENT ANSWER
# =====================================================

class StudentAnswer(models.Model):

    result = models.ForeignKey(
        Result,
        on_delete=models.CASCADE,
        related_name='answers'
    )

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='student_answers'
    )

    student_answer = models.TextField(
        blank=True
    )

    score = models.IntegerField(
        default=0
    )

    is_correct = models.BooleanField(
        default=False
    )

    def __str__(self):
        return (
            f"{self.result.student.name} - "
            f"Question {self.question.id}"
        )


# =====================================================
# FEEDBACK
# =====================================================

class Feedback(models.Model):

    result = models.OneToOneField(
        Result,
        on_delete=models.CASCADE,
        related_name='feedback'
    )

    score = models.FloatField(
        default=0
    )

    comments = models.TextField(
        blank=True
    )

    suggestions = models.TextField(
        blank=True
    )

    def __str__(self):
        return (
            f"Feedback - "
            f"{self.result.student.name}"
        )


# =====================================================
# AI API
# =====================================================

class AIAPI(models.Model):

    api_key = models.CharField(
        max_length=255
    )

    model = models.CharField(
        max_length=100
    )

    def __str__(self):
        return self.model