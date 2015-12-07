# -*- coding: utf-8 -*-
u"""
    This module contains the definitions of forms to be used in the application.
"""
import re
from wtforms import Form, validators
from wtforms.fields import FileField, IntegerField

__author__ = 'infante'


class SubtitleUploadForm(Form):
    u"""
        Implements the form used to upload a subtitles file with the desired time correction.
    """

    # file field to upload file
    subtitle_file = FileField(u'Subtitle File')
    # integer field to hold the desired time displacement
    adjustment = IntegerField(u'Time in seconds')
