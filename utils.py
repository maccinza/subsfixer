# -*- coding: utf-8 -*-
u"""

"""

import re
from datetime import datetime, timedelta

__author__ = 'infante'


def adjust_seconds(seconds):

    def replacement(match_obj):
        pattern = match_obj.group(0)
        time_obj = datetime.strptime(pattern, "%H:%M:%S")
        added_time = time_obj + timedelta(seconds=seconds)
        new_str_time = added_time.strftime("%H:%M:%S")
        return new_str_time

    return replacement


def fix_file(file_content, seconds):
    return re.sub(r'\d{2}\:\d{2}:\d{2}', adjust_seconds(seconds), file_content)


def verify_file(file_content, filename):

    regexp = re.compile(r'\d{2}\:\d{2}:\d{2}')
    return regexp.findall(file_content) and filename.endswith('.srt')
