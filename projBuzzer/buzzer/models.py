from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
'''class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.user
@receiver(post_save, sender=User)
def create_user_instructor(sender, instance, created, **kwargs):
    if created:
        Instructor.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_instructor(sender, instance, **kwargs):
    instance.instructor.save()
'''
class Classroom(models.Model):
    topic = models.CharField(max_length=200)
    instructor = models.ManyToManyField(User)
    def __str__(self):
        return self.topic

class QuizManager(models.Manager):
    def publish(self):
        question_list = Question.objects.filter(quiz=self)
        for questions in question_list:
            print (questions)
            choices_list = Choice.objects.filter(question=questions)
            for choice in choices_list:
                print (choice)

class Quiz(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    description = models.CharField(max_length=200,default='default')
    pub_date = models.DateTimeField('date published')
    is_published = models.BooleanField(default=False)
    def __str__(self):
        return self.description


class Question(models.Model):
    quiz = models.ForeignKey(Quiz,on_delete=models.CASCADE)
    question= models.CharField(max_length=200)
    solution = models.PositiveSmallIntegerField(blank=True)
    def __str__(self):
        return self.question

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    number = models.PositiveSmallIntegerField()
    option = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.option
