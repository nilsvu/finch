from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template import loader
from django import forms
import datetime

from .models import *
from .engine import *

def index(request):
    template = loader.get_template('service/index.html')
    return HttpResponse(template.render({ 'courses': Course.objects.all() }, request))


class CreateStudentForm(forms.Form):
    name = forms.CharField(label="Name", max_length=100, widget=forms.TextInput(attrs={ 'class': 'form-control' }))
    birthday = forms.DateField(label="Birthday", widget=forms.SelectDateWidget(attrs={ 'class': 'form-control' }))
    gender = forms.ChoiceField(choices=( ("female", "Female"), ("male", "Male"), ("other", "Other") ), widget=forms.Select(attrs={ 'class': 'form-control' }))
    originLanguageCode = forms.CharField(label="Mother tongue", max_length=10, widget=forms.TextInput(attrs={ 'class': 'form-control' }))

def prepare_course(request, course_id):
    template = loader.get_template('service/prepare_course.html')
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        create_student_form = CreateStudentForm(request.POST)
        if create_student_form.is_valid():
            student = Student.objects.get_or_create(**create_student_form.cleaned_data)
            return HttpResponseRedirect(reverse('take_course', args=(course_id, student.id)))

    create_student_form = CreateStudentForm()
    return HttpResponse(template.render({ 'course': course, 'create_student_form': create_student_form }, request))


def take_course(request, course_id, student_id):
    template = loader.get_template('service/take_course.html')
    student = get_object_or_404(Student, pk=student_id)
    course = get_object_or_404(Course, pk=course_id)
    choice = chooseVariations(course=course, student=student)
    return HttpResponse(template.render({ 'student': student, 'course': course, 'choice': choice }, request))


def edit_course(request, course_id):
    template = loader.get_template('service/edit_course.html')
    course = get_object_or_404(Course, pk=course_id)
    return HttpResponse(template.render({ 'course': course }, request))


def save_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    print(request.POST['course'])
    return HttpResponseRedirect(reverse('edit_course', args=(course_id)))
