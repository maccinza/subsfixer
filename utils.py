# -*- coding: utf-8 -*-
u"""
    This module contains helper functions to help on the task of fixing the timing synchronization of
    a subtitles file.
"""

import re
from datetime import datetime, timedelta

__author__ = 'infante'


def adjust_seconds(seconds):
    u"""
        This function defines and returns an inner function that uses its parameter to substitute a pattern in a string.

        Args:
            seconds (int): Integer value representing a time in seconds.

        Returns:
            replacement (function): Inner defined function with a bind to 'seconds' parameter.
    """

    def replacement(match_obj):
        u"""
            This nested function receives a matched object representing a time and tries to substitute it for another
            time, subtracting o adding seconds (outer function parameter) to it.

            Args:
                match_obj (re.MatchObject): MatchObject instance containing the matched time strings.

            Returns:
                new_str_time (string): String representing the time to be replaced into the original subtitles file.
        """

        # gets matched time string
        new_str_time = pattern = match_obj.group(0)

        try:
            # converts the time string to an actual time object
            time_obj = datetime.strptime(pattern, "%H:%M:%S")
            # tries to add or subtract the value in seconds to the time object
            added_time = time_obj + timedelta(seconds=seconds)
            # converts the time object back to its string representation and returns it
            new_str_time = added_time.strftime("%H:%M:%S")
            return new_str_time

        except ValueError:
            # in the case of a subtraction, it may happen that the final result is an invalid negative time
            # then, returns the same time value
            return new_str_time

    return replacement


def fix_file(file_content, seconds):
    u"""
        Receives a file content and a time in seconds and applies the function to adjust the time
        strings on the file content replacing them by a adding 'seconds' to them.

        Args:
            file_content (string): String with the subtitle file contents.
            seconds (int): Integer value representing a time displacement in seconds.

        Returns:
            string: Result of the time string substitution.
    """

    # returns the file content string result of the substitution of matched time strings in the file content
    return re.sub(r'\d{2}\:\d{2}:\d{2}', adjust_seconds(seconds), file_content)


def verify_file(file_content, filename):
    u"""
        Verifies if the received subtitles file contains the expected time expressions and has the correct extension.

        Args:
            file_content (string): String with the file content.
            filename (string): String with the file name and extension.

        Returns:
            bool: True if at least one expected expression is found and file extension is '.str', False otherwise
    """

    # compiles the regular expression to match times in the format of 'HH:MM:SS'
    regexp = re.compile(r'\d{2}\:\d{2}:\d{2}')
    # returns a bool result of trying to find at least one matched string and the expected file extension
    return regexp.findall(file_content) and filename.endswith('.srt')
