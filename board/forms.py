from django import forms
from django.core.exceptions import ValidationError

from .models import Ad, Response


class AdForm(forms.ModelForm):

    class Meta:
        model = Ad
        fields = (
                  'title',
                  'text',
                  'category',
                  'image',
                  'upload',
                  )

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        text = cleaned_data.get('text')

        if text == title:
            raise ValidationError('Заголовок и текст должны отличаться!')

        return cleaned_data


class ResponseForm(forms.ModelForm):

    class Meta:
        model = Response
        fields = ['message']

