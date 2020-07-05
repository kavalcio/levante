from django.db import models

# Create your models here.

class Room(models.Model):
    room_id = models.AutoField(primary_key=True)
    room_key = models.CharField(max_length=20)
    active = models.BooleanField()
    is_tutorial = models.BooleanField(default=False)
    user_list = models.TextField(default='{}')

    def __str__(self):
        return str(self.room_id)

# class User(models.Model):
#     id = models.AutoField(primary_key=True)
#     user_id = models.CharField(max_length=30)

#     def __str__(self):
#         return self.user_id

class Question(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

class Response(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    response_text = models.CharField(max_length=200)
    check = models.IntegerField(default=0)
    voteNum = models.IntegerField(default=0)
    user_id = models.IntegerField()
    def __str__(self):
        return self.response_text

class Comment(models.Model):
    response = models.ForeignKey(Response, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=200)
    def __str__(self):
        return self.comment_text