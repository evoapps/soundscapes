from django import forms

from crispy_forms.helper import FormHelper

from .models import Episode

class UploadEpisodeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UploadEpisodeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

    class Meta:
        model = Episode
        fields = ('mp3', )
