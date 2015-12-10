# -*- coding: utf-8 -*-
u"""
    This module contains the mapping of the routes to the handler functions for the requests submitted by the
    client side.
"""

from subsfixer import app
from flask.templating import render_template
from flask import request, make_response
from forms import SubtitleUploadForm
from utils import verify_file, fix_file

__author__ = 'infante'


# binds this handler function to respond to get and post requests to the app root url
@app.route('/', methods=['GET', 'POST'])
def handle_subtitles():
    u"""
        Handler function for root url.
        It shows the page in with an empty form in the case of a 'GET' request and.
        In the case of a 'POST' request, returns the repaired subtitles file when the form validates and successfully
        repairs it. When any step fails, returns the page with the form containing the error messages.
    """

    if request.method == "GET":
        # in the case of a 'GET' request, gets an instance of the form and renders the page with it
        subtitle_form = SubtitleUploadForm()
        return render_template('app.html', subtitle_form=subtitle_form)

    elif request.method == "POST":
        # in the case of a 'POST' request, gets an instance of the form populated with the request parameters on the
        # request and initializes auxiliary variables as None
        subtitle_form = SubtitleUploadForm(request.form)
        error = None
        filename = None
        result_content = None

        if subtitle_form.validate():
            # if the form contains valid data
            try:
                # reads uploaded file content
                file_data = request.files[subtitle_form.subtitle_file.name].read()
                # gets its filename
                filename = request.files[subtitle_form.subtitle_file.name].filename
                # and gets from the form the value in seconds to add or subtract from the time pattern matches
                seconds = int(request.form['adjustment'])

                if verify_file(file_data, filename):
                    # if the file content and its extension are compatible with the expectations, calls function to
                    # proceed with the file repairing and stores its results (repaired string with file content)
                    result_content = fix_file(file_data, seconds)
                else:
                    # otherwise, creates the error message to be shown to the user
                    error = "File is not in the expected format and/or does not contain expected content."
            except (AttributeError, KeyError):
                # with any error occurs, composes another erro message to be shown to the user
                error = "Something went wrong on your submission, please again to submit a valid file."

            if error:
                # if there is an error message, add it to the form errors and render the page with the form containing
                # the errors to be shown
                subtitle_form.errors['subtitle_file'] = error
                return render_template('app.html', subtitle_form=subtitle_form)

            else:
                # otherwise, returns the repaired file as an attachment
                response = make_response(result_content)
                response.headers["Content-Disposition"] = "attachment; filename={0}".format("fixed_" + filename)
                return response

        # renders the page again with the form erros if form does not validate
        return render_template('app.html', subtitle_form=subtitle_form)