from django.db import models
from .fields import AutocutCharField


class Consent(models.Model):
    """
    This model holds current and historical record.
    The current active consent has revoked_at set to None.
    An update operation will set revoked_at using auto_now.
    """
    SP_DISPLAYNAME_LENGTH = 80

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Consent Statement'
        unique_together = (('consentid', 'entityID', 'revoked_at'), )

    uid = models.CharField(default='', max_length=50, verbose_name='UserID')
    displayname = AutocutCharField(default='', max_length=SP_DISPLAYNAME_LENGTH)
    consentid = models.CharField(max_length=200)  # hash(userid + attribut set)
    entityID = models.CharField(null=False, max_length=1024, verbose_name='Identifier der Anwendung')
    sp_displayname = AutocutCharField(max_length=SP_DISPLAYNAME_LENGTH)
    consent_text = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Einwilligung vom', )
    revoked_at = models.DateTimeField(null=True, blank=True, auto_now=False, verbose_name='Zurückziehung vom', )

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.pre_save_clean()
        super().save(force_insert, force_update, using, update_fields)

    def pre_save_clean(self):
        for f in self._meta.fields:
            if isinstance(f, models.CharField):
                value = getattr(self, f.attname)
                value_short = value[:f.max_length]
                setattr(self, f.attname, value_short)




    def __str__(self):
        return self.entityID

    def __repr__(self):
        return self.entityID
