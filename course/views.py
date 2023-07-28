from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserProfileForm, CourseForm
from .models import UserProfile, Course, CourseFile

def homepage(request):
    # Add any necessary data or logic here
    return render(request, 'homepage.html')

def register_user(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request, 'You have successfully registered.')
            return redirect('login')
    else:
        user_form = UserCreationForm()
        profile_form = UserProfileForm()
    return render(request, 'register.html', {'user_form': user_form, 'profile_form': profile_form})


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            user_profile = user.userprofile
            if user_profile.user_type == 'instructor':
                return redirect('teacher_dashboard')
            elif user_profile.user_type == 'student':
                return redirect('student_dashboard')
            else:
                return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('login')


@login_required
def teacher_dashboard(request):
    courses = Course.objects.filter(user=request.user)

    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.user = request.user
            course.save()

            for file in request.FILES.getlist('files'):
                CourseFile.objects.create(course=course, file=file)

            return redirect('teacher_dashboard')

    else:
        form = CourseForm()

    context = {
        'courses': courses,
        'teacher': request.user,
        'form': form
    }
    return render(request, 'teacher_dashboard.html', context=context)


@login_required
def student_dashboard(request):
    user_profile = UserProfile.objects.get(user=request.user)

    if user_profile.user_type == 'student':
        student_plan = user_profile.plan
        if student_plan == 'free':
            courses = Course.objects.filter(course_type=student_plan)
        else:
            courses = Course.objects.all()

        context = {
            'courses': courses,
            'student_plan': student_plan
        }

        return render(request, 'student_dashboard.html', context)
    else:
        return redirect('dashboard')


@login_required
def upgrade_plan(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if user_profile.user_type == 'student':
        return render(request, 'payment_page.html')


@login_required
def payment_page(request):
    return redirect('payment_page')


@login_required
def payment_confirm(request):
    # course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        student = get_object_or_404(UserProfile, user=request.user)
        student.plan = 'premium'
        student.save()
        return redirect('student_dashboard')

    return render(request, 'payment_page.html')


@login_required
def view_course_contents(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'view_course_contents.html', {'course': course})


@login_required
def view_course_students(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    students = User.objects.filter(course=course)
    return render(request, 'view_course_students.html', {'course': course, 'students': students})


@login_required
def create_course(request):
    return render(request, 'create_course.html')




@login_required
def create_course_submit(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.user = request.user
            course.save()

            for file in request.FILES.getlist('files'):
                CourseFile.objects.create(course=course, file=file)

            return redirect('teacher_dashboard')


@login_required
def student_management_system(request):
    students = UserProfile.objects.filter(user_type='student')
    return render(request, 'student_management_system.html', {'students': students})


@login_required
def update_course(request, course_id):
    course = Course.objects.get(id=course_id)
    course_file = CourseFile.objects.filter(course=course)
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            course_file.delete()
            for file in request.FILES.getlist('files'):
                CourseFile.objects.create(course=course, file=file)
            return redirect('teacher_dashboard')
    else:
        form = CourseForm(instance=course)

    return render(request, 'update_course.html', {'form': form, 'course': course})
