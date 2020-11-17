from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):

    name = forms.CharField(label='Your name', max_length=100, required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Optional',
    }))

    body = forms.CharField(label='Join the discussion', max_length=500, widget=forms.Textarea(attrs={
        'placeholder': '500 characters max',
        'rows': '3',
    }))
    
    class Meta:
        model = Comment
        fields = ('name', 'body')