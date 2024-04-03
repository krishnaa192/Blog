from django.forms import ModelForm
from .models import *
from django import forms
from .models import Tags,Blog
#create_form


#submit_form

class SubmitForm(ModelForm):

    class Meta:
        model =Blog
        fields =['blog_title','desc','blog_image','blog','tags']
    
    widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }
    
    def __init__(self, *args, **kwargs):
        super(SubmitForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Type your comment',
        'id': 'usercomment',
        'rows': 4
    }))
    class Meta:
        model = Comment
        fields =('content',)