# -*- coding: utf-8 -*-

import os
from flask import Flask

# App configuration

app = Flask(__name__)
app.debug = False


if __name__ == "__main__":
    from views import *
    port = int(os.environ.get('PORT', 33507))
    app.run(host='0.0.0.0', port=port)
