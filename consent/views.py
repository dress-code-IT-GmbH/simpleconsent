import urllib
from django.conf import settings
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, Http404
from rest_framework import viewsets
from consent.models.consent import consent
from consent.serializers import MDstatementSerializer
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt

# @never_cache  TODO: make this working with CBV
class MDstatementViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = consent.objects.all()
    serializer_class = MDstatementSerializer


@never_cache
def getunsignedxml(request: HttpRequest, id: int) -> HttpResponse:
    if request.method == "GET":
        mds = consent.objects.get(id=id)
        ed_unsignedxml_urlencoded = urllib.parse.quote_plus(mds.ed_uploaded)
        response = HttpResponse(ed_unsignedxml_urlencoded, content_type="text/plain")
        response["Access-Control-Allow-Origin"] = settings.SIGPROXY_ORIGIN
        return response
    else:
        raise Http404("Only GET supported at this path")


# Manual test to set ed_signed to blank (use @csrf_exempt):
# `curl -X POST -d "signedxml=" localhost:8000/api/mdstatement/signedxml/<id>/`
@csrf_exempt
def postsignedxml(request: HttpRequest, id: int) -> HttpResponse:
    if request.method == "POST":
        mds = consent.objects.get(id=id)
        try:
            mds.ed_signed = request.POST['signedxml']
            if hasattr(settings, 'siglog_path'):
                with (settings.siglog_path / 'signedxml.xml').open('wb') as fd:
                    fd.write(mds.ed_signed)
            mds.save()
        except Exception as e:
            raise Http404("Error when updating MDStatement.ed_signed.\n" + str(e))
        else:
            response = HttpResponse('OK', content_type='text/plain')
            response["Access-Control-Allow-Origin"] = settings.SIGPROXY_ORIGIN
            return response
    else:
        raise Http404("Only POST supported at this path")


def getstarturl(id: int) -> str:
    return (
            settings.SIGPROXY_BASEURL +
            '?unsignedxml_url=' + settings.PVZD_ORIGIN + '/' + settings.SIGPROXYAPI_PADMIN_GETUNSIGNEDXML + str(id) + '/' +
            '&result_to=' + settings.PVZD_ORIGIN + '/' + settings.SIGPROXYAPI_PADMIN_POSTSIGNEDXML + str(id) + '/' +
            '&return=' + settings.PVZD_ORIGIN + '/admin/portaladmin/mdstatement/' + str(id) + '/' +
            '&sigtype=samled'
    )

def startsigning(request: HttpRequest, id: int) -> HttpResponse:

    if request.method == "GET":
        return HttpResponseRedirect(getstarturl(id))
    else:
        raise Http404("Only GET supported at this path")

