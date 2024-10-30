from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Student, Teacher
from .forms import StudentForm, TeacherRegistrationForm
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

@csrf_exempt
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'app/login.html', {'error': 'Invalid credentials'})
    return render(request, 'app/login.html')

@csrf_exempt
def register_view(request):
    if request.method == "POST":
        form = TeacherRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_view')
    else:
        form = TeacherRegistrationForm()
    return render(request, 'app/register.html', {'form': form})

@login_required
def home(request):
    try:
        teacher = Teacher.objects.get(user=request.user)
    except Teacher.DoesNotExist:
        return redirect('register')

    students = Student.objects.filter(teacher=teacher)
    form = StudentForm()
    return render(request, 'app/home.html', {'students': students, 'form': form})
@login_required
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            subject = form.cleaned_data['subject']
            marks = form.cleaned_data['marks']

            
            teacher = Teacher.objects.get(user=request.user)

            
            student, created = Student.objects.get_or_create(
                name=name, subject=subject, teacher=teacher,
                defaults={'marks': marks}
            )
            if not created:
                student.marks += marks
                student.save()
            return redirect('home')
    else:
        form = StudentForm()

    return render(request, 'app/home.html', {'form': form})

@login_required
def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        student.name = request.POST.get('name', student.name)
        student.subject = request.POST.get('subject', student.subject)
        student.marks = int(request.POST.get('marks', student.marks))
        student.save()
        return redirect('home')
    return render(request, 'app/edit.html', {'student': student})

@login_required
def delete_student(request, student_id):
    teacher = get_object_or_404(Teacher, user=request.user)
    student = get_object_or_404(Student, id=student_id, teacher=teacher)
    student.delete()
    return redirect('home')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login_view')
