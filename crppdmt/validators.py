import os
import sys
import datetime
from django.core.exceptions import ValidationError


def validate_file_extension(value):

    # OBS: control of file existence to avoid errors if file not changed while editing request
    if os.path.isfile(value.name):
        ext = os.path.splitext(value.name)[1].lower()
        valid_extensions = ['.pdf']
        if not ext in valid_extensions:
            raise ValidationError(u'File type not supported! ' + ext)


def validate_file_size(value):

    # OBS: control of file existence to avoid errors if file not changed while editing request
    if os.path.isfile(value.name):
        file_size = value.file.size
        megabyte_limit = 2.0
        if file_size > megabyte_limit*1024*1024:
            raise ValidationError("Max file size is %sMB" % str(megabyte_limit))

def validate_date_greater_than_today(value):

    diff = value - datetime.datetime.date(datetime.datetime.now())
    if int(diff.days) <= 0:
        raise ValidationError("Date must be greater than today!")