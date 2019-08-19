from django.forms import ModelForm
from consent.models import Consent

class ConsentForm(ModelForm):

    class Meta:
        model = Consent
        exclude = []

    def clean(self):
        # TODO ...
        cleaned_data = super().clean()

