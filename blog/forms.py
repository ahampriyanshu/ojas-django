from django import forms
from .models import Comment
from captcha.fields import CaptchaField

class CommentForm(forms.ModelForm):

    name = forms.CharField(label='Your name', max_length=100, required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Optional','class': 'p-2 rounded border border-gray-200 bg-white dark:border-gray-700 text-gray-600 dark:text-gray-200 focus:bg-white focus:outline-none focus:ring-2 focus:ring-teal-400 focus:border-transparent placeholder-gray-400 text-sm h-auto'
    }))

    body = forms.CharField(label='Enter your message', max_length=500, widget=forms.Textarea(attrs={
        'placeholder': '500 characters max','class': 'p-2 rounded border border-gray-200 bg-white dark:border-gray-700 text-gray-600 dark:text-gray-200 focus:bg-white focus:outline-none focus:ring-2 focus:ring-teal-400 focus:border-transparent placeholder-gray-400 text-sm h-auto','rows': '3',
    }))

    captcha = CaptchaField(label='Verify you are a human')
    
    class Meta:
        model = Comment
        fields = ('name',  'captcha', 'body',)