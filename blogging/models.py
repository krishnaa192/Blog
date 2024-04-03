from distutils.command.upload import upload
from operator import truediv
from pickle import TRUE
from django.db import models
from django.contrib.auth.models import User
import uuid
from user.models import Profile
from ckeditor.fields import RichTextField




class Tags(models.Model):
    name=models.CharField(max_length=9)
    created=models.DateTimeField(auto_now_add=TRUE)
    
   
    class Meta:
        ordering=['created']

    def __str__(self):
        return self.name 


class Blog(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True,unique=False)
    Author=models.ForeignKey(Profile,on_delete=models.CASCADE,name="Author", null="True")
    blog=RichTextField()
    blog_title=models.CharField(max_length=33)
    desc=models.CharField(max_length=100, null=True)
    
    blog_image = models.ImageField( upload_to='media/images/blogs',default='ppp.jpg',
        null=True, blank=True)
    Pen_name=models.CharField(max_length=7)
    tags=models.ForeignKey(Tags, on_delete=models.CASCADE,null=True,blank=True,name="tags")
    upload=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['upload']

    def __str__(self):
        return self.blog_title    
    

class Subscribe(models.Model):
    email = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    post = models.ForeignKey('Blog', related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Character(models.Model):
    name=models.CharField(max_length=33)
    age=models.IntegerField()
    description=models.TextField()
 

    def __str__(self):
        return self.name




class StoryPart(models.Model):
    CONTENT_TYPES = [
        ('story', 'Story'),
        ('poem', 'Poem'),
        ('novel', 'Novel'),
        ('short_story', 'Short Story'),
        ('essay', 'Essay'),
        ('drama', 'Drama'),
        ('script', 'Script'),
        ('article', 'Article'),
        ('review', 'Review'),
        ('other', 'Other'),
    ]
    conent_restrictions = [
        ('adult', 'Adult'),
        ('teen', 'Teen'),
        ('everyone', 'Everyone'),
    ]
    status=[
        ('draft','Draft'),
        ('published','Published')

    ]

    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True,unique=False)
    Author=models.ForeignKey(Profile,on_delete=models.CASCADE,name="Author", null="True")
    story=RichTextField()
    story_title=models.CharField(max_length=33)
    desc=models.CharField(max_length=200, null=True)
    story_image = models.ImageField( upload_to='media/images/stories',default='ppp.jpg',
        null=True, blank=True)
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPES)
    content_restrictions = models.CharField(max_length=20, choices=conent_restrictions)

    upload=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=20, choices=status)

    def __str__(self):
        return self.story_title
    



class Story(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    story_title = models.CharField(max_length=100)
    story = models.ForeignKey(StoryPart, on_delete=models.CASCADE, related_name='parts')
    part_number = models.PositiveIntegerField()
    part_desc = RichTextField()

    def __str__(self):
        return f"Part {self.part_number} of {self.story.story_title}"