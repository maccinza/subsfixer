# -*- coding: utf-8 -*-
u"""

"""

from server import app
from flask.templating import render_template
from flask import request
from forms import SubtitleUploadForm

__author__ = 'infante'


@app.route('/', methods=['GET', 'POST'])
def handle_subtitles():
    if request.method == "GET":
        subtitle_form = SubtitleUploadForm()
        return render_template('app.html', subtitle_form=subtitle_form)
    elif request.method == "POST":
        subtitle_form = SubtitleUploadForm(request.form)
        if subtitle_form.validate():
            subtitle_data = request.files[subtitle_form.subtitle_file.name].read()
            print subtitle_data
            # TODO: verificar extensao e se possui faixas de tempo
            # TODO: tratar erros/ trabalhar o arquivo e retornar download
        return render_template('app.html', subtitle_form=subtitle_form)

