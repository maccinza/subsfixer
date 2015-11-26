# -*- coding: utf-8 -*-
u"""

"""

from server import app
from flask.templating import render_template
from flask import request, make_response
from forms import SubtitleUploadForm
from utils import verify_file, fix_file
from configs import FILE_TTL

__author__ = 'infante'


@app.route('/', methods=['GET', 'POST'])
def handle_subtitles():

    if request.method == "GET":

        subtitle_form = SubtitleUploadForm()
        return render_template('app.html', subtitle_form=subtitle_form)

    elif request.method == "POST":
        # TODO: change behavior to store file for some time and return url for downloading the file
        subtitle_form = SubtitleUploadForm(request.form)
        error = None
        filename = None
        result_content = None

        if subtitle_form.validate():
            try:
                file_data = request.files[subtitle_form.subtitle_file.name].read()
                filename = request.files[subtitle_form.subtitle_file.name].filename
                seconds = int(request.form['adjustment'])
                if verify_file(file_data, filename):
                    result_content = fix_file(file_data, seconds)
                else:
                    error = "File is not in the expected format and/or does not contain expected content."
            except (AttributeError, KeyError):
                error = "Something went wrong on your submission, please again to submit a valid file."

            if error:
                subtitle_form.errors['subtitle_file'] = error
                return render_template('app.html', subtitle_form=subtitle_form)

            else:
                response = make_response(result_content)
                response.headers["Content-Disposition"] = "attachment; filename={0}".format("fixed_" + filename)
                return response

        return render_template('app.html', subtitle_form=subtitle_form)