from django.contrib.auth.models import User
from django.db import models

from django.dispatch import receiver
from django.db.models.signals import post_save

TYPE_OF_TEST = (
    ('Descriptive', 'descriptive'),
    ('Test', 'test'),
    ('T/F', 't/f'),
)

QS_ANSWER = (
    ('o_1', 1),
    ('o_2', 2),
    ('o_3', 3),
    ('o_4', 4),
)


class Exam(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    classroom = models.CharField(max_length=65)
    exam_duration = models.IntegerField()
    teacher_name = models.CharField(max_length=65)
    type_of_exam = models.CharField(choices=TYPE_OF_TEST, max_length=20)
    exam_url = models.URLField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    # exam_score = models.IntegerField()


# Filling in the exam_url field
@receiver(post_save, sender=Exam)
def add_url(sender, instance, **kwargs):
    url = 'http://127.0.0.1:8000/exam/%s/' % instance.id
    instance.exam_url = url


class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    question = models.CharField(max_length=450)
    option_1 = models.CharField(max_length=250)
    option_2 = models.CharField(max_length=250)
    option_3 = models.CharField(max_length=250)
    option_4 = models.CharField(max_length=250)
    # qs_score = models.IntegerField()
    answer = models.CharField(max_length=25, choices=QS_ANSWER)


class Student(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    email = models.EmailField()
    score = models.IntegerField()


class StudentAnswer(models.Model):
    qs = models.ForeignKey(Question, on_delete=models.CASCADE)
    stu = models.ForeignKey(Student, on_delete=models.CASCADE)
    answer = models.CharField(max_length=15, choices=QS_ANSWER, blank=True, null=True)
    correct_or_not = models.BooleanField(default=False)


# @receiver(post_save, sender=StuQs)
# def add_score(sender, instance, **kwargs):
#     if instance.correct_or_not:
#         instance.stu.score += instance.qs.qs_score
#     # Student.score += Question.qs_score


# class AnswerSheet(models.Model):
#     exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
#     student = models.ForeignKey(Student, on_delete=models.CASCADE)
#     score = models.IntegerField()
#     answered_questions = models.ManyToManyField(Question, related_name='answered_questions')
#     wrong_questions = models.ManyToManyField(Question, related_name='wrong_questions')
#     not_answered = models.ManyToManyField(Question, related_name='not_answered')
