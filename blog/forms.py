from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'shadow appearance-none border rounded py-2 px-3 text-grey-darker',
        'placeholder': 'Enter Your Name',
    }))

    email = forms.EmailField(widget=forms.TextInput(attrs={
        'class': 'shadow appearance-none border rounded py-2 px-3 text-grey-darker',
        'placeholder': 'Not Mandatory',
    }))

    body = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'mx-auto px-3 mb-2 mt-2 bg-gray-100 rounded border border-gray-400 leading-normal resize-none w-full h-20 py-2 px-3 font-medium placeholder-gray-700 focus:outline-none focus:bg-white',
        'placeholder': 'Type your comment',
        'rows': '4',
        'coloumns':'50',
    }))
    
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')