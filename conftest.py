import pytest
import django
from django.conf import settings

@pytest.fixture(scope='session', autouse=True)
def setup_django():
    if not settings.configured:  # ⚡️ Oldin sozlanganini tekshiramiz
        settings.configure(DJANGO_SETTINGS_MODULE="Core.settings")
    django.setup()  # ⚡️ Django ni ishga tushirish
