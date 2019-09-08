from django.contrib import admin
from django.db import models

from consent.models import Consent

@admin.register(Consent)
class ConsentAdmin(admin.ModelAdmin):
    list_display = (
        'userid',
        'entityID',
        'sp_displayname',
        'consent_text',
        'created_at',
        'revoked_at',
    )