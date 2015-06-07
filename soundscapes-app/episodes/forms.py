from django import forms

from .models import Show

class ShowForm(forms.ModelForm):

    class Meta:
        model = Show
        fields = ('name', 'rss_url')

    def save(self, *args, **kwargs):
        show = super(ShowForm, self).save(*args, **kwargs)
        show.refresh()
        return show
