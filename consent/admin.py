from django.contrib import admin

from consent.models import Consent


@admin.register(Consent)
class ConsentAdmin(admin.ModelAdmin):
    list_display = (
        'consentid',
        'entityID',
        'sp_displayname',
        'consent_text',
        'created_at',
        'revoked_at',
    )
