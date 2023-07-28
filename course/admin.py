from django.contrib import admin

from course.models import Course, CourseFile, UserProfile

admin.site.register(Course)
admin.site.register(CourseFile)
admin.site.register(UserProfile)
