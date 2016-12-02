from django.shortcuts import render,redirect, render_to_response,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Classroom
from buzzer.models import *
from django.template import loader

from django.contrib import admin

from django.conf import settings

#from buzzer.quizform import QuizForm
# Create your views here.
@login_required(login_url=settings.WEBSITE_URL)
def home(request):
    Classrooms = Classroom.objects.filter(instructor = request.user)
    Quizes = Quiz.objects.all()
    template = loader.get_template('home.html')
    context = {
        'Classrooms': Classrooms,
        'Quizes':Quizes,
    }
    return HttpResponse(template.render(context, request))

def thanks(request, quiz_id):
    template = loader.get_template('thanks.html')
    context = { 'quiz_id' : quiz_id,
                'WEBSOCKET_URL': settings.WEBSOCKET_URL,
            }
    return HttpResponse(template.render(context, request))

def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

def display_quiz(request,quiz_id):
    #classroom = Classroom.objects.filter(instructor=user_id).filter(id = classroom_id)
    #quiz = Quiz.objects.filter(classroom = classroom).filter(id = quiz_id)
    quiz = Quiz.objects.get(pk=quiz_id)
    if(quiz.is_published):
        question_list = Question.objects.filter(quiz=quiz)
        choice_list = []
        for questions in question_list:
            choices_list = Choice.objects.filter(question=questions)
            for choice in choices_list:
                choice_list.append(choice)
        template = loader.get_template('quiz.html')
        context = {
        'question_list': question_list,
        'choice_list' : choice_list,
        'quiz_id' : quiz_id,
        'quiz_name': quiz.description,
        }
    else :
        template = loader.get_template('quiz.html')
        context = {}
    return HttpResponse(template.render(context, request))

def vote(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    question_list = Question.objects.filter(quiz=quiz)
    for question in question_list:
        try:
            selected_choice = Choice.objects.get(pk=request.POST['choice'+str(question.id)])
        except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
            return render(request, 'buzzer/publish/'+str(quiz_id)+'.html', {
                'question': question,
                'error_message': "You didn't select a choice.",
                })
        else:
            selected_choice.votes += 1
            selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
    return HttpResponseRedirect('thanks/'+str(quiz_id))

@login_required(login_url=settings.WEBSITE_URL)
def results(request, quiz_id):
    quiz = Quiz.objects.get(pk=quiz_id)
    question_list = Question.objects.filter(quiz=quiz)
    choice_list = []
    for questions in question_list:
        choices_list = Choice.objects.filter(question=questions)
        for choice in choices_list:
            choice_list.append(choice)
    template = loader.get_template('results.html')
    context = {
        'question_list': question_list,
        'choice_list' : choice_list,
        'quiz_id' : quiz_id,
        'quiz_name': quiz.description,
        'WEBSOCKET_URL': settings.WEBSOCKET_URL,

}
    return HttpResponse(template.render(context, request))

def quiz(request):
    i = request.POST['id']
    return HttpResponseRedirect('/buzzer/quiz/' +str(i) )

@login_required(login_url=settings.WEBSITE_URL)
def publish(request,quiz_id):
    if(request.user.is_authenticated):
        quiz = Quiz.objects.get(pk=quiz_id)
        quiz.is_published = True
        quiz.save()
    return HttpResponseRedirect('/buzzer' )

@login_required(login_url=settings.WEBSITE_URL)
def unpublish(request,quiz_id):
    if(request.user.is_authenticated):
        quiz = Quiz.objects.get(pk=quiz_id)
        quiz.is_published = False
        quiz.save()
    return HttpResponseRedirect('/buzzer' )

@login_required(login_url=settings.WEBSITE_URL)
def clear(request,quiz_id):
    if(request.user.is_authenticated):
        quiz = Quiz.objects.get(pk=quiz_id)
        question_list = Question.objects.filter(quiz=quiz)
        for questions in question_list:
            choices_list = Choice.objects.filter(question=questions)
            for choice in choices_list:
                choice.votes = 0
                choice.save()
    return HttpResponseRedirect('/buzzer' )

'''
def quiz_form(request):
    form = QuizForm(request.POST or None)
    if form.is_valid():
        #do_something_with(form.cleaned_data)
        return redirect("create_user_success")
    return render_to_response("signup/form.html", {'form': form})
'''
