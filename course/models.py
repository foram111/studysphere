from django.db import models
from django.contrib.auth.models import User


USER_TYPES = (
    ('student', 'student'),
    ('instructor', 'instructor'),
)

COURSE_TYPES = (
    ('free', 'free'),
    ('premium', 'premium')
)

STUDENT_PLAN_CHOICES = (
    ('free', 'Free Plan'),
    ('premium', 'Premium Plan'),
)

GRADE_CHOICES = (
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    ('F', 'F'),
)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    user_type = models.CharField(choices=USER_TYPES, max_length=20)
    plan = models.CharField(max_length=10, choices=STUDENT_PLAN_CHOICES, blank=True, null=True)
    grade = models.CharField(max_length=3, choices=GRADE_CHOICES, blank=True, null=True)
    attendance = models.CharField(max_length=100, blank=True, null=True)


class Course(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='course_instructor',
                             null=True, blank=True)
    title = models.CharField(max_length=80)
    total_hours = models.IntegerField(null=True, blank=True)
    description = models.CharField(max_length=500)
    course_type = models.CharField(choices=COURSE_TYPES, max_length=20)


class CourseFile(models.Model):
    course = models.ForeignKey(Course, related_name='course_file', on_delete=models.CASCADE)
    file = models.FileField(upload_to='documents/')

