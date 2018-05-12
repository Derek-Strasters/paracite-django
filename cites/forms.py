from django import forms
from django.contrib.auth.models import User


class NewStory(forms.Form):
    title = forms.CharField(label='Title',
                            max_length=255,
                            widget=forms.TextInput(
                                attrs={  # TODO: I don't like th here...
                                    'class': 'form-control'}))
    paragraph = forms.CharField(label='First Paragraph',
                                max_length=4095,
                                widget=forms.Textarea(attrs={
                                    'class': 'form-control',
                                    'placeholder': 'Enter the first paragraph',
                                    'rows': '7'}))


class NewParagraph(forms.Form):
    paragraph = forms.CharField(label='New Paragraph',
                                max_length=4095,
                                help_text='Enter the first paragraph',
                                widget=forms.Textarea(attrs={
                                    'class': 'form-control',
                                    'placeholder': 'Enter the first paragraph',
                                    'rows': '7'}))


class UserCreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class UserLoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']
