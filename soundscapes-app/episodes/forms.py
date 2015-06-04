from django import forms

from .models import Show, Episode

class ShowForm(forms.ModelForm):

    class Meta:
        model = Show
        fields = ('name', 'rss')

class UploadEpisodeMP3Form(forms.ModelForm):

    class Meta:
        model = Episode
        fields = ('mp3', )
