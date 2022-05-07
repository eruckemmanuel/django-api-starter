import logging

from django.conf import settings


APP_ID = getattr(settings, 'APP_ID', '')


def get_headers(request):
    headers = request.META
    return headers


class RequestLogFormatter(logging.Formatter):
    def format(self, record):
        record.message = record.getMessage()
        record.app_id = APP_ID

        try:
            request = record.request
        except Exception as e:
            request = None

        if request:
            record.http_method = request.method
            record.path_info = request.path
            record.data = request.POST
            record.params = request.GET

            if request.user and request.user.is_authenticated:
                record.username = request.user.username

            record.headers = get_headers(request)
        else:
            record.http_method = ""
            record.path_info = ""
            record.data = ""
            record.params = ""

            record.headers = ""

        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)
        s = self.formatMessage(record)
        if record.exc_info:
            # Cache the traceback text to avoid converting it multiple times
            # (it's constant anyway)
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            if s[-1:] != "\n":
                s = s + "\n"
            s = s + record.exc_text
        if record.stack_info:
            if s[-1:] != "\n":
                s = s + "\n"
            s = s + self.formatStack(record.stack_info)
        return s
