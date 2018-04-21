from django import forms


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
                                widget=forms.Textarea(attrs={
                                    'class': 'form-control',
                                    'placeholder': 'Enter the first paragraph',
                                    'rows': '7'}))
