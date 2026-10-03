from django.contrib import admin

from .models import (
    Login,
    Technology,
    Question,
    Result,
    StudentAnswer,
    Feedback,
    AIAPI,
)


@admin.register(Login)
class LoginAdmin(admin.ModelAdmin):
    list_display = ("name", "email")
    search_fields = ("name", "email")


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = (
        "technology_name",
        "category",
        "total_questions",
        "duration",
    )
    search_fields = ("technology_name",)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        "question_text",
        "technology",
        "difficulty",
    )
    list_filter = (
        "technology",
        "difficulty",
    )
    search_fields = (
        "question_text",
    )


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "technology",
        "score",
        "total_questions",
        "percentage",
        "date",
    )
    list_filter = (
        "technology",
    )


@admin.register(StudentAnswer)
class StudentAnswerAdmin(admin.ModelAdmin):
    list_display = (
        "result",
        "question",
        "score",
        "is_correct",
    )
    list_filter = (
        "is_correct",
    )


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = (
        "result",
        "score",
    )


@admin.register(AIAPI)
class AIAPIAdmin(admin.ModelAdmin):
    list_display = (
        "model",
    )