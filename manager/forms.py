from django import forms
from django.core.urlresolvers import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Show, Segment

class ShowForm(forms.ModelForm):

    class Meta:
        model = Show
        fields = ('name', 'slug', 'rss_url')

    def __init__(self, *args, **kwargs):
        super(ShowForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('show_create')
        self.helper.add_input(Submit('submit', 'Add'))

    def save(self, *args, **kwargs):
        show = super(ShowForm, self).save(*args, **kwargs)
        show.refresh()
        return show

class SegmentForm(forms.ModelForm):

    class Meta:
        model = Segment
        fields = ('start_time', 'end_time')

    def __init__(self, *args, **kwargs):
        super(SegmentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        #self.helper.form_action = reverse('segment_create')
        self.helper.add_input(Submit('submit', 'Create'))
