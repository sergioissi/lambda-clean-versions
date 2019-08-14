import logging
import json
import traceback
import json_logging
from pytz import timezone
from datetime import datetime


json_logging.ENABLE_JSON_LOGGING = True

TimeZone = timezone('Europe/Rome')


def extra(**kw):
    """
    Add the required nested has_extra layer
    """
    return {'extra': {'has_extra': kw}}


class CustomJSONLog(logging.Formatter):
    """
    Customized logger
    """
    def get_exc_fields(self, record):
        if record.exc_info:
            exc_info = self.format_exception(record.exc_info)
        else:
            exc_info = record.exc_text
        return {f'exc_info': exc_info}

    @classmethod
    def format_exception(cls, exc_info):
        return ''.join(traceback.format_exception(*exc_info)) if exc_info else ''

    def format(self, record):
        json_log_object = {"datetime": datetime.now(TimeZone).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
                           "level": record.levelname,
                           "processId": record.process,
                           "message": record.getMessage()
                           }

        if hasattr(record, 'has_extra'):
            json_log_object.update(record.has_extra)

        json_log_object['logger'] = {
            f'logger_name': record.name,
            f'module': record.module,
            f'funcName': record.funcName,
            f'filename': record.filename,
            f'lineno': record.lineno,
            f'thread': f'{record.threadName}[{record.thread}]'
        }

        if record.exc_info or record.exc_text:
            json_log_object['logger'].update(self.get_exc_fields(record))

        return json.dumps(json_log_object)


def logger_init():
    json_logging.__init(custom_formatter=CustomJSONLog)
