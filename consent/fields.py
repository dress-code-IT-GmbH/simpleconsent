from django.db import models
from django.utils.translation import ugettext_lazy as _


class AutocutCharField(models.CharField):
    description = _(
        "CharField that is autocut to max_length")

    def _cut_by_max_length(self, value):
        return value[:self.max_length]

    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        value = self._cut_by_max_length(value)
        return self.to_python(value)
