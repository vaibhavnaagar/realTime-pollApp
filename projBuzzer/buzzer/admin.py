from django.contrib import admin
from buzzer.models import *

# Register your models here.
#dmin.site.register(Instructor)
class ChoiceInLine(admin.StackedInline):
        model = Choice
        extra = 1

class QuizInLine(admin.StackedInline):
        model = Quiz
        extra = 1

class QuizAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['classroom']}),
        (None, {'fields': ['description']}),
        (None, {'fields': ['pub_date']}),
        (None, {'fields': ['is_published']}),

    ]

    def get_queryset(self, request):
        temp=super(QuizAdmin,self).get_queryset(request).filter(classroom=-100)
        classrooms = Classroom.objects.filter(instructor = request.user)
        for classs in classrooms:
            temp = temp | super(QuizAdmin,self).get_queryset(request).filter(classroom=classs)

        return temp

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['quiz']}),
        (None, {'fields': ['question']}),
        (None, {'fields': ['solution']}),
    ]
    inlines = [ChoiceInLine]
    def get_queryset(self, request):
        temp = super(QuestionAdmin,self).get_queryset(request).filter(quiz=-100)
        tempQuiz = Quiz.objects.filter(classroom = -1)
        classrooms = Classroom.objects.filter(instructor = request.user)
        for classs in classrooms:
            tempQuiz = tempQuiz | Quiz.objects.filter(classroom = classs)

        for quizz in tempQuiz:
            temp = temp | super(QuestionAdmin,self).get_queryset(request).filter(quiz=quizz)

        return temp

class ClassroomAdmin(admin.ModelAdmin):

    fieldsets = [
        (None, {'fields': ['topic']}),
        (None, {'fields': ['instructor']}),
    ]
    inlines = [QuizInLine]
    def get_queryset(self, request):
            return super(ClassroomAdmin,self).get_queryset(request).filter(instructor=request.user)


admin.site.register(Classroom,ClassroomAdmin)
admin.site.register(Quiz,QuizAdmin)
admin.site.register(Question,QuestionAdmin)
#admin.site.register(Choice)
