from django.db import models

# Create your models here.

class Room(models.Model):
    id = models.AutoField(primary_key=True)
    room_key = models.CharField(max_length=20)
    active = models.BooleanField()

    def __str__(self):
        return self.room_key

# class User(models.Model):
#     id = models.AutoField(primary_key=True)
#     user_id = models.CharField(max_length=30)

#     def __str__(self):
#         return self.user_id

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

class Response(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    response_text = models.CharField(max_length=200)
    nominations = models.IntegerField(default=0)
    developed = models.IntegerField(default=0)
    voted = models.IntegerField(default=0)
    def __str__(self):
        return self.response_text

class Comment(models.Model):
    response = models.ForeignKey(Response, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=200)
    def __str__(self):
        return self.comment_text