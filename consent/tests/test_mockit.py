import pytest
from consent.models import Consent


@pytest.mark.django_db()
def test_mokit():
    nc = Consent(
        uid='1234',
        displayname='This is a much too long displayname to be displayed in a sensible way because it is too long',
        consentid='Foobar',
        entityID='Foobar',
        sp_displayname='This is a much too long displayname to be displayed in a sensible way because it is too long',
    )
    nc.save()
    stored = Consent.objects.get(uid='1234')
    assert(len(stored.displayname) == stored.SP_DISPLAYNAME_LENGTH)
    assert(len(stored.sp_displayname) == stored.SP_DISPLAYNAME_LENGTH)
    return None


def test_pre_save_clean():
    nc = Consent(
        uid='1234',
        displayname='This is a much too long displayname to be displayed in a sensible way because it is too long',
        consentid='Foobar',
        entityID='Foobar',
        sp_displayname='This is a much too long displayname to be displayed in a sensible way because it is too long',
    )
    nc.pre_save_clean()
    assert(len(nc.displayname) == nc.SP_DISPLAYNAME_LENGTH)
    assert(len(nc.sp_displayname) == nc.SP_DISPLAYNAME_LENGTH)
    return None
