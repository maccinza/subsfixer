# -*- coding: utf-8 -*-
u"""

"""
import re
from wtforms import Form, validators
from wtforms.fields import FileField, IntegerField

__author__ = 'infante'


class SubtitleUploadForm(Form):
    subtitle_file = FileField(u'Subtitle File')
    adjustment = IntegerField(u'Time in seconds')

