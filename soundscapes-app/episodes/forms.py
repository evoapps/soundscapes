from django import forms

from crispy_forms.helper import FormHelper

from .handlers import get_meta_data
from .models import Episode

class UpdateEpisodeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UpdateEpisodeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

    class Meta:
        model = Episode
        fields = ('show', 'released', 'title', 'mp3')

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
            episode.look_up()
            episode.save()

        return episode
