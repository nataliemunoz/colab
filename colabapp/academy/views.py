from django.shortcuts import render
from .models import Course, Subscription, Subject, Student
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect
from django.contrib import messages


# Create your views here.

def v_index(request):
    context = {
        'course1' : Course.objects.get(name = 'Matematica Avanzada'),
        'course2' : Course.objects.get(name = 'Literatura')
    }
    return render(request, 'index.html', context) #nelaza la vista con el html

def v_course(request, course_id):
    context = {
        'course': Course.objects.get(id = course_id)
    }

     # traer el ultimo subject de un curso
    subject = Subject.objects.filter(course_id = course_id).last()
    if subject is None:
        return HttpResponseRedirect("/") #rdirigir al home, inicio

    context['subs'] = subject

    if request.user.is_authenticated:
        if Student.objects.filter(id = request.user.id).exists(): #true si existe
            #estoy 100% seguro que se trata de un estudiante
            verificar = Subscription.objects.filter(subject_id = subject.id, student_id = request.user.id).exists() # retorna true o false
            # verificar es true, el estudiante se ha suscrito
            # verificar es False, no existe un registre, el estudiante no suscrito
            context['subscribed'] = verificar

    return render(request, 'course.html', context)  

@login_required(login_url = "/admin/login")
@permission_required('academy.add_subscription', login_url = "/admin/login")
def v_subscribe(request, course_id):
    # traer el ultimo subject de un curso
    subject = Subject.objects.filter(course_id = course_id).last()
    if subject is None:
        messages.error(request,"No puedes subscribirte a este curso")
        return HttpResponseRedirect("/academy/course/%s" % (course_id))

    #filter => where course_id = 12 and studend_id = 33
    verificar = Subscription.objects.filter(subject_id = subject.id, student_id = request.user.id)
    if verificar.exists():
        messages.success(request,"Tu subscripcion ya esta activa")
        return HttpResponseRedirect("/academy/course/%s" % (course_id))
    else:
        subs = Subscription()
        subs.student_id = request.user.id
        subs.subject_id = subject.id
        subs.save()
        messages.success(request,"En buena hora, acabas de subscribirte!")
        return HttpResponseRedirect("/academy/course/%s" % (course_id))


