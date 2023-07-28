from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from course import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name='homepage'),  # Set homepage.html as the default homepage
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('teacher_dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('upgrade_plan/', views.upgrade_plan, name='upgrade_plan'),
    path('payment-page/', views.payment_page, name='payment_page'),
    path('payment-confirm/', views.payment_confirm, name='payment_confirm'),
    path('view-course-contents/<int:course_id>/', views.view_course_contents, name='view_course_contents'),
    path('view-course-students/<int:course_id>/', views.view_course_students, name='view_course_students'),
    path('create-course/', views.create_course, name='create_course'),
    path('create-course-submit/', views.create_course_submit, name='create_course_submit'),
    path('student-management-system/', views.student_management_system, name='student_management_system'),
    path('teacher_dashboard/update_course/<int:course_id>/', views.update_course, name='update_course'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)