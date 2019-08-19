from django.contrib import admin
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseRedirect
from django.db import models
from django.forms.widgets import ClearableFileInput

from consent.forms import ConsentForm
from consent.models.consent import Consent
from consent.views import getstarturl
#from PVZDpy.samlentitydescriptor import SAMLEntityDescriptor
#from PVZDpy.get_seclay_request import get_seclay_request


class FileInputWidget(ClearableFileInput):
    template_name = 'portaladmin/widgets/clearable_file_input.html'


@admin.register(consent)
class MDstatementAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.FileField: {'widget': FileInputWidget},
    }
    change_form_template = "portaladmin/md_statement_admin_change_form.html"
    form = MDstatementForm
    save_on_top = True
    readonly_fields = (
        'id',
        'content_valid',
        'created_at',
        'ed_signed',
        'ed_uploaded',
        'ed_uploaded_filename',
        'entityID',
        'signer_subject',
        'namespace',
        'operation',
        'org_cn',
        'org_id',
        'signer_authorized',
        'status',
        'updated_at',
        'validation_message',
    )
    list_display = (
        'entity_fqdn',
        'status',
        'content_valid',
        'signer_authorized',
        'operation',
        'namespace',
        'org_id',
        'signer_subject',
        'get_validation_message_trunc',
        'updated',
        'admin_note',
    )
    list_display_links = ('entity_fqdn', 'status')
    list_filter = (
        'status',
        'namespace',
        'org_id',
        'signer_subject',
    )
    search_fields = (
        'entity_fqdn',
        'status',
        'operation',
        'namespace',
        'org_id',
        'signer_subject',
        'admin_note',
    )
    fieldsets = (
        ('Entity', {
            'fields': (
                'entityID',
                'operation',
            )
        }),
        ('Prozess Status', {
            'fields': (
                'status',
                'content_valid',
                'signer_authorized',
                'validation_message',
            )
        }),
        ('Neue Datei hochladen', {
            'fields': (
                'ed_file_upload',
                'ed_uploaded_filename',
            )
        }),
        ('Administrative Attribute', {
            'fields': (
                'admin_note',
                ('created_at', 'updated_at', ),
                'signer_subject',
                'allow_selfsigned',
                'id',
            )
        }),
        ('EntityDescriptor XML', {
            'classes': ('collapse',),
            'fields': (
                'ed_signed',
                'ed_uploaded',
            ),
        }),
    )

#    def get_urls(self):
#        urls = super().get_urls()
#        custom_urls = [
#            path('get_signature_request/<int:id>/request.xml',
#                 self.get_signature_request_view,
#                 name='portaladmin_get_signature_request'),
#        ]
#        return custom_urls + urls

    def get_fieldsets(self, request, obj=None):
        ''' return only 1st and 3rd fieldsets on add views '''
        from copy import deepcopy
        fieldsets = deepcopy(super(MDstatementAdmin, self).get_fieldsets(request, obj))
        if obj:  # change request
            return fieldsets
        else:
            return (fieldsets[2], fieldsets[3])

    def response_add(self, request, obj, post_url_continue=None):
        if 'Sign' in request.POST:
            raise ValidationError('Signatur kann nicht erstellt werden bevor die Eingabe gesichert wird.')
        return super().response_add(request, obj, post_url_continue=None)

    def response_change(self, request, obj):
        if 'Sign' in request.POST:
            url = getstarturl(obj.id)
            return HttpResponseRedirect(url)
        else:
            return super().response_change(request, obj)

    #actions = ['delete_selected', ]  # for dev
    #actions = []

