from rest_framework import serializers
from consent.models.consent import consent


class MDstatementSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = consent
        fields = (
            'userid',
            'entityID',
            'revoked_at',
            'sp_displayname',
            'consent_text',
            'created_at',
        )

