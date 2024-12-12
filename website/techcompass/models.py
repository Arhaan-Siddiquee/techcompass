from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError



def validate_svg(file):
    if not file.name.endswith('.svg'):
        raise ValidationError(u'Error message')

class Roadmap(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    badge = models.FileField(upload_to='badges/',blank=True,null=True,validators=[validate_svg])
    created_at = models.DateTimeField(auto_now_add=True)
    #updated_at = models.DateTimeField(auto_now=True)
    courses_provided = models.ManyToManyField('Course', related_name='roadmaps', blank=True)

    def __str__(self):
        return self.title
    
class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    #image = models.ImageField(upload_to='courses/')
    created_at = models.DateTimeField(auto_now_add=True)
    #updated_at = models.DateTimeField(auto_now=True)
    related_to = models.ForeignKey(Roadmap, on_delete=models.CASCADE, related_name='courses')

    videos = models.JSONField(default=list, blank=True)

    def __str__(self):
        return self.title
    
class Progress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress')
    roadmap = models.ForeignKey(Roadmap, on_delete=models.CASCADE, related_name='progress')
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    completed_courses = models.ManyToManyField(Course, related_name='progress', blank=True)

    def __str__(self):
        return f'{self.user.username} - {self.roadmap.title}'

