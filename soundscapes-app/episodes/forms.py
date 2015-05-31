from django import forms

from crispy_forms.helper import FormHelper

from .models import Episode

class UploadEpisodeForm(forms.ModelForm):
    look_up_on_save = forms.BooleanField(required = False)

    def __init__(self, *args, **kwargs):
        super(UploadEpisodeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

    class Meta:
        model = Episode
        fields = ('mp3', )

    def save(self, *args, **kwargs):
        episode = super(UploadEpisodeForm, self).save(*args, **kwargs)

        if self.cleaned_data['look_up_on_save']:
            episode.link_to_soundcloud()
            episode.save()

        return episode
