from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):

    body = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': '500 characters max',
        'rows': '3',
    }))
    
    class Meta:
        model = Comment
        fields = ('name', 'body')