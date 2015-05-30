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
        fields = ('show', 'number', 'name', 'mp3')

class UploadEpisodeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UploadEpisodeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

    class Meta:
        model = Episode
        fields = ('mp3', )

    def save(self, *args, **kwargs):
        episode = super(UploadEpisodeForm, self).save(*args, **kwargs)

        meta_data = get_meta_data(episode.mp3.url)
        update_episode_form = UpdateEpisodeForm(instance = episode,
                                                data = meta_data)

        if update_episode_form.is_valid():
            episode = update_episode_form.save()

        return episode
