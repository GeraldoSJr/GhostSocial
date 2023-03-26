from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    datePost = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User ,default = "Excluido", on_delete=models.SET_DEFAULT)

    def __str__(self):
        return self.title

