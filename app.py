# -*- coding: utf-8 -*-
u"""

"""
import os
from flask import Flask

__author__ = 'infante'

app = Flask(__name__)
app.debug = False

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
