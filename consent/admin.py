from django.contrib import admin

from consent.models import Consent


@admin.register(Consent)
class ConsentAdmin(admin.ModelAdmin):
    list_display = (
        'uid',
        'displayname',
        'consentid',
        'entityID',
        'sp_displayname',
        'created_at',
        'revoked_at',
    )
