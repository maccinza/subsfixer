# -*- coding: utf-8 -*-
u"""

"""
from flask import Flask

__author__ = 'infante'

app = Flask(__name__)
app.debug = False

if __name__ == "__main__":
    app.run()

