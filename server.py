# -*- coding: utf-8 -*-

import os
from flask import Flask

# App configuration

app = Flask(__name__)
app.debug = False

port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)
