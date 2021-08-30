from django.contrib.staticfiles.storage import StaticFilesStorage as BaseStaticFilesStorage
from django.conf import settings


class StaticFilesStorage(BaseStaticFilesStorage):
    def url(self, name):
        return '%s?v=%s' % (super().url(name), settings.VERSION)
