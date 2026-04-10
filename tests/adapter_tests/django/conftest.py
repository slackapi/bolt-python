import os

import django

os.environ["DJANGO_SETTINGS_MODULE"] = "tests.adapter_tests.django.test_django_settings"
django.setup()
