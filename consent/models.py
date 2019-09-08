import json
from django.db import models

class Consent(models.Model):
    """
    This model holds current and historical record.
    The current active consent has revoked_at set to None.
    An update operation will set revoked_at using auto_now.
    """
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Consent Statement'
        unique_together = (('userid', 'entityID', 'revoked_at'), )

    userid = models.CharField(max_length=200)
    entityID = models.CharField(null=False, max_length=1024, verbose_name='Identifier der Anwendung')
    sp_displayname = models.CharField(max_length=80)
    consent_text = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Einwilligung vom', )
    revoked_at = models.DateTimeField(null=True, blank=True, auto_now=False, verbose_name='Zurückziehung vom', )


#-------
#    def serialize_json(self):
#        """ serialize stable values for unit tests """
#        dictfilt = lambda d, filter: dict([(k, d[k]) for k in d if k in set(filter)])
#        wanted_keys = (
#            'userid',
#            'entityID',
#            'sp_displayname',
#            'consent_text',
#            'created_at',
#            'revoked_at',
#    )
#        self_dict = dictfilt(self.__dict__, wanted_keys)
#        return json.dumps(self_dict, sort_keys=True, indent=2)

    def __str__(self):
        return self.entityID
